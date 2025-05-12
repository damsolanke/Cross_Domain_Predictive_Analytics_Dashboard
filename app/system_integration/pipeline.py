"""
Data pipeline for real-time processing.
"""
import time
import threading
import logging
from typing import Dict, Any, List, Callable

class DataPipeline:
    """Data processing pipeline for the system."""
    
    def __init__(self):
        """Initialize the data pipeline."""
        self.start_timestamp = time.time()
        self.processors = {}
        self.data_sources = {}
        self.processing_thread = None
        self.is_running = False
        self.processing_queue = []
        self.logger = logging.getLogger(__name__)
        
    def register_processor(self, name: str, processor_fn: Callable):
        """
        Register a data processor function.
        
        Args:
            name: Processor name
            processor_fn: Processor function that takes data as input and returns processed data
        """
        self.processors[name] = processor_fn
        self.logger.info(f"Registered processor: {name}")
        return self
        
    def register_data_source(self, name: str, data_source):
        """
        Register a data source.
        
        Args:
            name: Data source name
            data_source: Data source object
        """
        self.data_sources[name] = data_source
        self.logger.info(f"Registered data source: {name}")
        return self
        
    def start_processing(self):
        """Start the data processing thread."""
        if self.is_running:
            self.logger.warning("Pipeline is already running")
            return
            
        self.is_running = True
        self.processing_thread = threading.Thread(target=self._process_loop)
        self.processing_thread.daemon = True
        self.processing_thread.start()
        self.logger.info("Started data processing thread")
        
    def stop_processing(self):
        """Stop the data processing thread."""
        self.is_running = False
        if self.processing_thread:
            self.processing_thread.join(timeout=2.0)
        self.logger.info("Stopped data processing thread")
        
    def _process_loop(self):
        """Main processing loop that runs in a thread."""
        while self.is_running:
            if self.processing_queue:
                try:
                    item = self.processing_queue.pop(0)
                    self._process_item(item)
                except Exception as e:
                    self.logger.error(f"Error processing data: {e}")
            else:
                time.sleep(0.1)  # Avoid busy waiting
                
    def _process_item(self, item: Dict[str, Any]):
        """
        Process a single data item through all registered processors.
        
        Args:
            item: Data item to process
        """
        result = item
        for name, processor in self.processors.items():
            try:
                result = processor(result)
            except Exception as e:
                self.logger.error(f"Error in processor {name}: {e}")
                # Continue with unmodified data
        
        return result
        
    def submit_data(self, data: Dict[str, Any]) -> bool:
        """
        Submit data for processing.
        
        Args:
            data: Data to process
            
        Returns:
            True if data was queued successfully
        """
        if not self.is_running:
            self.logger.warning("Cannot submit data - pipeline is not running")
            return False
            
        self.processing_queue.append(data)
        return True
        
    def get_current_timestamp(self) -> float:
        """Get the current timestamp."""
        return time.time()
        
    def get_uptime(self) -> float:
        """Get the pipeline uptime in seconds."""
        return time.time() - self.start_timestamp
        
    def check_system_health(self) -> Dict[str, Any]:
        """
        Check the health of the system.
        
        Returns:
            Health status information
        """
        return {
            'status': 'healthy',
            'uptime': self.get_uptime(),
            'processors': len(self.processors),
            'data_sources': len(self.data_sources),
            'queue_size': len(self.processing_queue)
        }