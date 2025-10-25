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

    def connect_to_live(self, username):
        """Connect to TikTok live stream"""
        try:
            self.username = username
            self.log_message.emit(f"Connecting to @{username}...")

            # Create client
            self.client = TikTokLiveClient(unique_id=f"@{username}")

            # Register event handlers
            self._register_events()

            # Start connection in thread
            self.log_message.emit("Starting connection...")
            self.log_message.emit("This may take 10-30 seconds...")
            self.client.run()

        except TimeoutError as e:
            error_msg = f"Connection timeout: User '{username}' might not be live or username is incorrect"
            self.error_occurred.emit(error_msg)
            self.log_message.emit(error_msg)
            self.connection_status.emit("Timeout - Not Live?")
        except Exception as e:
            error_type = type(e).__name__
            if "ReadTimeout" in error_type or "Timeout" in str(e):
                error_msg = f"Connection timeout: User @{username} might not be live right now"
            else:
                error_msg = f"Connection error ({error_type}): {str(e)}"
            self.error_occurred.emit(error_msg)
            self.log_message.emit(error_msg)
            self.connection_status.emit("Connection Failed")
            traceback.print_exc()

    def disconnect_from_live(self):
        """Disconnect from TikTok live stream"""
        try:
            if self.client:
                self.log_message.emit("Stopping connection...")

                # Stop the client properly
                try:
                    self.client.disconnect()
                except:
                    pass

                try:
                    self.client.stop()
                except:
                    pass

                self.client = None
                self.is_connected = False
                self.connection_status.emit("Disconnected")
                self.log_message.emit("Disconnected successfully")
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
            """Handle disconnection"""
            self.is_connected = False
            self.connection_status.emit("Disconnected")
            self.log_message.emit("Connection lost")

            # Auto-reconnect
            if self.reconnect_attempts < config.MAX_RECONNECT_ATTEMPTS:
                self.reconnect_attempts += 1
                self.log_message.emit(
                    f"Reconnecting... (Attempt {self.reconnect_attempts}/"
                    f"{config.MAX_RECONNECT_ATTEMPTS})"
                )
                # Reconnect logic would go here

        @self.client.on(JoinEvent)
        async def on_join(event: JoinEvent):
            """Handle user join event"""
            try:
                user = event.user
                event_data = {
                    'type': 'join',
                    'username': user.nickname or user.unique_id,
                    'user_id': user.unique_id,
                    'avatar_url': user.avatar.avatar_url if hasattr(user, 'avatar') else '',
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
                    'avatar_url': user.avatar.avatar_url if hasattr(user, 'avatar') else '',
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
                    'avatar_url': user.avatar.avatar_url if hasattr(user, 'avatar') else '',
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
                    'avatar_url': user.avatar.avatar_url if hasattr(user, 'avatar') else '',
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
                    'avatar_url': user.avatar.avatar_url if hasattr(user, 'avatar') else '',
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
                    'avatar_url': user.avatar.avatar_url if hasattr(user, 'avatar') else '',
                    'like_count': like_count,
                    'timestamp': event.timestamp if hasattr(event, 'timestamp') else None
                }

                # Only emit for every 10 likes to avoid spam
                if like_count % 10 == 0:
                    self.event_received.emit(event_data)
                    self.log_message.emit(f"👍 {event_data['username']} sent {like_count} likes")

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
