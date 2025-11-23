"""
TikTok Live Event Handler
Manages connection to TikTok live stream and processes events
"""

from PyQt6.QtCore import QObject, pyqtSignal, QThread
from TikTokLive import TikTokLiveClient
from TikTokLive.events import (ConnectEvent, DisconnectEvent, CommentEvent,
                               GiftEvent, JoinEvent, ShareEvent,
                               FollowEvent, LikeEvent)
import config
import traceback
import asyncio
import httpx


def get_avatar_url(user):
    """
    Get avatar URL from user object with multiple fallbacks
    Based on TikTokLive API - tries various avatar fields
    """
    # Try different avatar fields in order of preference (larger to smaller)
    avatar_fields = [
        ('avatar_thumb', 'm_urls'),     # Found in logs: ImageModel(m_urls=[...])
        ('avatar_thumb', 'url_list'),   # Common in TikTokLive (UserImage object)
        ('avatar_medium', 'url_list'),  # Medium avatar
        ('avatar_large', 'url_list'),   # Large avatar
        ('avatar_url', None),           # Direct URL (API style)
        ('avatar', 'avatar_url'),       # Standard avatar object
        ('avatarLarge', None),          # Large avatar URL
        ('avatarMedium', None),         # Medium avatar URL
        ('avatar', 'urls'),             # Avatar URLs array
        ('avatarSmall', None),          # Small avatar URL
        ('profilePictureUrl', None),    # Alternative field name
    ]

    for field_name, sub_field in avatar_fields:
        try:
            if hasattr(user, field_name):
                field_value = getattr(user, field_name)

                if field_value:
                    # If sub_field is specified (e.g. 'url_list' or 'avatar_url')
                    if sub_field:
                        if hasattr(field_value, sub_field):
                            url = getattr(field_value, sub_field)
                            if url and isinstance(url, str) and url.startswith('http'):
                                print(f"[DEBUG] Found avatar URL for {user.unique_id}: {url}")
                                return url
                            # For lists (like url_list or m_urls)
                            elif isinstance(url, (list, tuple)) and len(url) > 0:
                                final_url = url[0]
                                print(f"[DEBUG] Found avatar URL (from list) for {user.unique_id}: {final_url}")
                                return final_url
                        # For 'urls' which might be an array
                        elif sub_field == 'urls' and isinstance(field_value, (list, tuple)) and len(field_value) > 0:
                            url = field_value[0]
                            print(f"[DEBUG] Found avatar URL (from list) for {user.unique_id}: {url}")
                            return url
                    # No sub-field, direct URL string
                    elif isinstance(field_value, str) and field_value.startswith('http'):
                        print(f"[DEBUG] Found avatar URL (direct) for {user.unique_id}: {field_value}")
                        return field_value
        except Exception:
            continue
            
    print(f"[DEBUG] No avatar URL found for user {user.unique_id}")
    return None


class TikTokHandler(QObject):
    """
    Handles TikTok Live connection and events
    Emits signals for UI updates
    """

    # Signals
    event_received = pyqtSignal(dict)  # Event data
    connection_status = pyqtSignal(str)  # Status message
    error_occurred = pyqtSignal(str)  # Error message
    log_message = pyqtSignal(str)  # Log message

    def __init__(self):
        super().__init__()

        self.client = None
        self.username = ""
        self.is_connected = False
        self.reconnect_attempts = 0
        self.http_client = None
        self.should_reconnect = True  # Flag to control reconnection

    def connect_to_live(self, username):
        """Connect to TikTok live stream with auto-retry and reconnect"""
        self.username = username
        self.should_reconnect = True  # Enable reconnection
        clean_username = username.lstrip('@')

        # Cleanup old connection if exists
        if self.client:
            try:
                self.log_message.emit("[CLEANUP] Closing old connection...")
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self._async_cleanup())
                loop.close()
            except Exception as e:
                self.log_message.emit(f"[CLEANUP] Old connection cleanup: {str(e)}")
            self.client = None

        # Create or reuse httpx client with longer timeout
        if not self.http_client:
            self.log_message.emit("[INIT] Creating HTTP client with extended timeout...")
            self.http_client = httpx.AsyncClient(
                timeout=httpx.Timeout(90.0, connect=45.0),  # 90s read, 45s connect
                follow_redirects=True,
                limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
                http2=True  # Enable HTTP/2
            )

        # Retry loop for initial connection + auto-reconnect
        attempt = 0
        max_initial_retries = 3

        while self.should_reconnect:
            try:
                attempt += 1

                # Create client with custom settings
                self.log_message.emit("[INIT] Creating TikTok Live client...")
                self.client = TikTokLiveClient(
                    unique_id=clean_username,
                    web_proxy=None,
                    ws_proxy=None
                )

                # Inject custom http client with longer timeout
                self.client._web._client = self.http_client

                # Register event handlers ONCE per client
                self._register_events()

                # Start connection
                if attempt == 1:
                    self.log_message.emit(f"Connecting to @{username}...")
                    self.log_message.emit("[WAIT] This may take 30-90 seconds...")
                    self.log_message.emit(f"[CONNECTING] Attempting to connect to @{clean_username}'s live stream...")
                else:
                    self.log_message.emit(f"[RECONNECT] Attempt {attempt}...")

                # Run the client (blocks until disconnected)
                self.client.run()

                # If we get here, connection ended (disconnected)
                self.log_message.emit("[INFO] Connection ended")

                # Check if we should reconnect
                if not self.should_reconnect:
                    self.log_message.emit("[INFO] Auto-reconnect disabled, stopping")
                    break

                # Check reconnect attempts limit
                if self.reconnect_attempts >= config.MAX_RECONNECT_ATTEMPTS:
                    self.log_message.emit(f"[ERROR] Max reconnection attempts ({config.MAX_RECONNECT_ATTEMPTS}) reached")
                    self.connection_status.emit("Connection Failed - Max Retries")
                    break

                # Wait before reconnecting with exponential backoff
                self.reconnect_attempts += 1
                wait_seconds = min(5 * self.reconnect_attempts, 30)
                self.log_message.emit(
                    f"[RECONNECT] Attempt {self.reconnect_attempts}/"
                    f"{config.MAX_RECONNECT_ATTEMPTS} in {wait_seconds}s..."
                )
                self.connection_status.emit(f"Reconnecting ({self.reconnect_attempts}/{config.MAX_RECONNECT_ATTEMPTS})...")

                import time
                time.sleep(wait_seconds)

            except (TimeoutError, httpx.ReadTimeout, httpx.ConnectTimeout) as e:
                error_msg = f"[WARNING] Connection timeout (attempt {attempt}): User '@{username}' might not be live"
                self.error_occurred.emit(error_msg)
                self.log_message.emit(error_msg)

                # Retry initial connection failures
                if attempt < max_initial_retries:
                    wait_seconds = 5 * attempt
                    self.log_message.emit(f"[RETRY] Retrying in {wait_seconds}s... ({attempt}/{max_initial_retries})")
                    import time
                    time.sleep(wait_seconds)
                    continue
                else:
                    self.log_message.emit("[TIP] Troubleshooting:")
                    self.log_message.emit("   1. Make sure the user is LIVE right now")
                    self.log_message.emit("   2. Check your internet connection")
                    self.log_message.emit("   3. Try again later")
                    self.connection_status.emit("Timeout - User Not Live?")
                    break

            except Exception as e:
                error_type = type(e).__name__
                error_str = str(e)

                # Better error messages based on error type
                if "ReadTimeout" in error_type or "Timeout" in error_str:
                    error_msg = f"[WARNING] Connection timeout: @{username} might not be live"
                elif "UserOffline" in error_str or "not live" in error_str.lower():
                    error_msg = f"[ERROR] User @{username} is not currently live"
                elif "Invalid" in error_str or "not found" in error_str.lower():
                    error_msg = f"[ERROR] Username '{username}' not found or invalid"
                else:
                    error_msg = f"[ERROR] Connection error: {error_str}"

                self.error_occurred.emit(error_msg)
                self.log_message.emit(error_msg)
                self.connection_status.emit("Connection Failed")
                traceback.print_exc()

                # Retry initial connection failures
                if attempt < max_initial_retries and "not live" not in error_str.lower():
                    wait_seconds = 5 * attempt
                    self.log_message.emit(f"[RETRY] Retrying in {wait_seconds}s... ({attempt}/{max_initial_retries})")
                    import time
                    time.sleep(wait_seconds)
                    continue
                else:
                    break

    async def _async_cleanup(self):
        """Async cleanup of client connection"""
        if self.client:
            try:
                await self.client.disconnect()
            except Exception:
                pass

    def disconnect_from_live(self):
        """Disconnect from TikTok live stream (user-initiated, disables reconnect)"""
        try:
            # Disable auto-reconnect when user manually disconnects
            self.should_reconnect = False
            self.reconnect_attempts = 0

            if self.client:
                self.log_message.emit("Stopping connection...")

                # Stop the client properly with async handling
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(self._async_cleanup())
                    loop.close()
                except Exception as e:
                    self.log_message.emit(f"[CLEANUP] Disconnect: {str(e)}")

                self.client = None
                self.is_connected = False
                self.connection_status.emit("Disconnected")
                self.log_message.emit("[OK] Disconnected successfully")

            # Cleanup HTTP client on manual disconnect
            if self.http_client:
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(self.http_client.aclose())
                    loop.close()
                    self.http_client = None
                    self.log_message.emit("[CLEANUP] HTTP client closed")
                except Exception as e:
                    self.log_message.emit(f"[CLEANUP] HTTP client: {str(e)}")

        except Exception as e:
            error_msg = f"Disconnect error: {str(e)}"
            self.error_occurred.emit(error_msg)
            self.log_message.emit(error_msg)

    def _register_events(self):
        """Register TikTok event handlers"""

        @self.client.on(ConnectEvent)
        async def on_connect(event: ConnectEvent):
            """Handle successful connection"""
            self.is_connected = True
            self.reconnect_attempts = 0
            status_msg = f"Connected to @{self.username}'s live!"
            self.connection_status.emit(status_msg)
            self.log_message.emit(status_msg)

        @self.client.on(DisconnectEvent)
        async def on_disconnect(event: DisconnectEvent):
            """Handle disconnection - reconnection is handled by outer loop"""
            self.is_connected = False
            self.connection_status.emit("Disconnected")
            self.log_message.emit("[DISCONNECT] Connection lost")
            # Note: Reconnection logic is now in connect_to_live() main loop

        @self.client.on(JoinEvent)
        async def on_join(event: JoinEvent):
            """Handle user join event"""
            try:
                user = event.user
                event_data = {
                    'type': 'join',
                    'username': user.nickname or user.unique_id,
                    'user_id': user.unique_id,
                    'avatar_url': get_avatar_url(user) or '',
                    'timestamp': event.timestamp if hasattr(event, 'timestamp') else None
                }

                self.event_received.emit(event_data)
                self.log_message.emit(f"👋 {event_data['username']} joined")

            except Exception as e:
                self.log_message.emit(f"Error processing join event: {str(e)}")

        @self.client.on(CommentEvent)
        async def on_comment(event: CommentEvent):
            """Handle comment event"""
            try:
                user = event.user
                event_data = {
                    'type': 'comment',
                    'username': user.nickname or user.unique_id,
                    'user_id': user.unique_id,
                    'avatar_url': get_avatar_url(user) or '',
                    'comment': event.comment,
                    'timestamp': event.timestamp if hasattr(event, 'timestamp') else None
                }

                self.event_received.emit(event_data)
                self.log_message.emit(f"💬 {event_data['username']}: {event.comment}")

            except Exception as e:
                self.log_message.emit(f"Error processing comment event: {str(e)}")

        @self.client.on(GiftEvent)
        async def on_gift(event: GiftEvent):
            """Handle gift event"""
            try:
                user = event.user
                gift = event.gift

                event_data = {
                    'type': 'gift',
                    'username': user.nickname or user.unique_id,
                    'user_id': user.unique_id,
                    'avatar_url': get_avatar_url(user) or '',
                    'gift_name': gift.name if hasattr(gift, 'name') else 'Gift',
                    'gift_id': gift.id if hasattr(gift, 'id') else 0,
                    'gift_count': event.repeat_count if hasattr(event, 'repeat_count') else 1,
                    'timestamp': event.timestamp if hasattr(event, 'timestamp') else None
                }

                self.event_received.emit(event_data)
                self.log_message.emit(
                    f"🎁 {event_data['username']} sent {event_data['gift_name']} "
                    f"x{event_data['gift_count']}"
                )

            except Exception as e:
                self.log_message.emit(f"Error processing gift event: {str(e)}")

        @self.client.on(ShareEvent)
        async def on_share(event: ShareEvent):
            """Handle share event"""
            try:
                user = event.user
                event_data = {
                    'type': 'share',
                    'username': user.nickname or user.unique_id,
                    'user_id': user.unique_id,
                    'avatar_url': get_avatar_url(user) or '',
                    'timestamp': event.timestamp if hasattr(event, 'timestamp') else None
                }

                self.event_received.emit(event_data)
                self.log_message.emit(f"🔗 {event_data['username']} shared the live")

            except Exception as e:
                self.log_message.emit(f"Error processing share event: {str(e)}")

        @self.client.on(FollowEvent)
        async def on_follow(event: FollowEvent):
            """Handle follow event"""
            try:
                user = event.user
                event_data = {
                    'type': 'follow',
                    'username': user.nickname or user.unique_id,
                    'user_id': user.unique_id,
                    'avatar_url': get_avatar_url(user) or '',
                    'timestamp': event.timestamp if hasattr(event, 'timestamp') else None
                }

                self.event_received.emit(event_data)
                self.log_message.emit(f"❤️ {event_data['username']} followed")

            except Exception as e:
                self.log_message.emit(f"Error processing follow event: {str(e)}")

        @self.client.on(LikeEvent)
        async def on_like(event: LikeEvent):
            """Handle like event"""
            try:
                user = event.user
                like_count = event.count if hasattr(event, 'count') else 1

                event_data = {
                    'type': 'like',
                    'username': user.nickname or user.unique_id,
                    'user_id': user.unique_id,
                    'avatar_url': get_avatar_url(user) or '',
                    'like_count': like_count,
                    'timestamp': event.timestamp if hasattr(event, 'timestamp') else None
                }

                # Emit ALL likes - user wants every like to count for points
                self.event_received.emit(event_data)
                # Log only every 5 likes to avoid log spam
                if like_count % 5 == 0:
                    self.log_message.emit(f"[LIKE] {event_data['username']} sent {like_count} likes")

            except Exception as e:
                self.log_message.emit(f"Error processing like event: {str(e)}")


class TikTokThread(QThread):
    """
    Thread to run TikTok client without blocking UI
    """

    def __init__(self, handler, username):
        super().__init__()
        self.handler = handler
        self.username = username

    def run(self):
        """Run the TikTok client"""
        try:
            self.handler.connect_to_live(self.username)
        except Exception as e:
            self.handler.error_occurred.emit(f"Thread error: {str(e)}")
            traceback.print_exc()
