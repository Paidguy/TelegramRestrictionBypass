"""Worker bot management for handling multiple bot instances."""

import itertools
from typing import Optional, List
from pyrogram import Client
from pyrogram.errors import AuthKeyUnregistered, AccessTokenInvalid

from logger import LOGGER
from config import PyroConf
from helpers.settings import Config
from constants import (
    WORKER_BOT_WORKERS,
    WORKER_BOT_MAX_TRANSMISSIONS,
    SLEEP_THRESHOLD,
    DOWNLOADS_DIR
)


class WorkerManager:
    """Manages multiple bot workers for load distribution."""

    def __init__(self, main_bot: Client):
        """Initialize worker manager with main bot.
        
        Args:
            main_bot: The primary bot instance
        """
        self.worker_pool: List[Client] = [main_bot]
        self.worker_iterator: Optional[itertools.cycle] = None

    def get_next_worker(self) -> Client:
        """Get the next available worker from the pool.
        
        Returns:
            Client: An available worker bot
        """
        if not self.worker_pool:
            return self.worker_pool[0]

        if not self.worker_iterator:
            self.worker_iterator = itertools.cycle(self.worker_pool)

        # Try to find a connected worker
        for _ in range(len(self.worker_pool)):
            try:
                worker = next(self.worker_iterator)
                if worker.is_connected:
                    return worker
            except StopIteration:
                self.worker_iterator = itertools.cycle(self.worker_pool)

        # Fallback to first worker
        return self.worker_pool[0]

    async def start_new_worker(self, token: str, is_temp: bool = False) -> Optional[str]:
        """Start a new worker bot and add it to the pool.
        
        Args:
            token: Bot token to use for the worker
            is_temp: Whether this is a temporary worker (not saved to config)
            
        Returns:
            str: Name of the added bot, or None if failed
        """
        try:
            bot_id = token.split(":")[0]
        except (ValueError, IndexError):
            LOGGER(__name__).error(f"Invalid token format: {token}")
            return None

        try:
            # Create new worker with optimized settings for downloads
            new_worker = Client(
                f"worker_{bot_id}",
                api_id=PyroConf.API_ID,
                api_hash=PyroConf.API_HASH,
                bot_token=token,
                workers=WORKER_BOT_WORKERS,
                sleep_threshold=SLEEP_THRESHOLD,
                max_concurrent_transmissions=WORKER_BOT_MAX_TRANSMISSIONS,
                ipv6=False,
                no_updates=True,
                workdir=DOWNLOADS_DIR
            )
            await new_worker.start()

            me = new_worker.me
            if not me:
                await new_worker.stop()
                LOGGER(__name__).error(f"Failed to get bot info for {bot_id}")
                return None

            # Check if worker already exists
            for worker in self.worker_pool:
                if worker.me.id == me.id:
                    if not is_temp:
                        await new_worker.stop()
                    LOGGER(__name__).info(f"Worker {me.first_name} already exists")
                    return me.first_name

            # Add to pool
            self.worker_pool.append(new_worker)
            self.worker_iterator = itertools.cycle(self.worker_pool)

            LOGGER(__name__).info(f"Worker Added: {me.first_name} ({me.id})")
            
            if not is_temp:
                Config.add_extra_bot(token)

            return me.first_name

        except Exception as e:
            LOGGER(__name__).error(f"Failed to start worker {bot_id}: {e}")
            return None

    async def stop_worker(self, bot_id: str) -> bool:
        """Stop and remove a worker from the pool.
        
        Args:
            bot_id: ID of the bot to remove
            
        Returns:
            bool: True if worker was removed, False otherwise
        """
        target = None
        for worker in self.worker_pool:
            if str(worker.me.id) == str(bot_id):
                target = worker
                break

        if not target:
            LOGGER(__name__).warning(f"Worker {bot_id} not found")
            return False

        # Don't remove the main bot
        if target.bot_token == PyroConf.BOT_TOKENS[0]:
            LOGGER(__name__).warning("Cannot remove main bot")
            return False

        # Remove from pool
        self.worker_pool.remove(target)
        self.worker_iterator = itertools.cycle(self.worker_pool)

        try:
            Config.remove_extra_bot(target.bot_token)
            await target.stop()
            LOGGER(__name__).info(f"Worker {bot_id} stopped and removed")
        except Exception as e:
            LOGGER(__name__).error(f"Error stopping worker {bot_id}: {e}")

        return True

    def get_worker_count(self) -> int:
        """Get the number of active workers.
        
        Returns:
            int: Number of workers in the pool
        """
        return len(self.worker_pool)

    def get_workers(self) -> List[Client]:
        """Get all workers in the pool.
        
        Returns:
            List[Client]: List of all worker clients
        """
        return self.worker_pool.copy()

    async def is_worker_valid(self, worker: Client) -> bool:
        """Check if a worker is still valid and connected.
        
        Args:
            worker: The worker client to check
            
        Returns:
            bool: True if worker is valid, False otherwise
        """
        try:
            return worker.is_connected and worker.me is not None
        except (AuthKeyUnregistered, AccessTokenInvalid):
            return False
        except Exception:
            return False
