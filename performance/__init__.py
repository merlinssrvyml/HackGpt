"""
Performance and Scalability Module

This module provides performance optimization and scalability features for HackGPT,
including caching, parallel processing, load balancing, and performance monitoring.
"""

from .cache_manager import CacheManager, RedisCache, MemoryCache
from .parallel_processor import ParallelProcessor, TaskQueue
from .performance_monitor import PerformanceMonitor, MetricsCollector
from .load_balancer import LoadBalancer, HealthChecker
from .optimization import QueryOptimizer, ResourceOptimizer

__version__ = "1.0.0"

__all__ = [
    'CacheManager',
    'RedisCache', 
    'MemoryCache',
    'ParallelProcessor',
    'TaskQueue',
    'PerformanceMonitor',
    'MetricsCollector',
    'LoadBalancer',
    'HealthChecker',
    'QueryOptimizer',
    'ResourceOptimizer'
]
