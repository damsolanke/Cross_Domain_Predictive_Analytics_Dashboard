"""
Integration module for the Cross-Domain Predictive Analytics Dashboard.
"""

# System integrator instance (shared globally)
class SystemIntegrator:
    """
    Integrates various components of the system.
    """
    
    def __init__(self):
        """Initialize the system integrator."""
        self.data_pipeline = None
        self.components = {}
        
    def init_pipeline(self):
        """Initialize the data pipeline."""
        from app.system_integration.pipeline import DataPipeline
        self.data_pipeline = DataPipeline()
        return self.data_pipeline
        
    def register_component(self, name, component):
        """Register a component with the system."""
        self.components[name] = component
        return component
        
    def get_component(self, name):
        """Get a component by name."""
        return self.components.get(name)


# Create a global system integrator instance
system_integrator = SystemIntegrator()

def init_system_integration(app):
    """Initialize system integration with an app."""
    # Initialize data pipeline
    pipeline = system_integrator.init_pipeline()
    
    # Register other components
    from app.system_integration.cross_domain_correlation import CrossDomainCorrelator
    from app.system_integration.cross_domain_prediction import CrossDomainPredictor
    from app.system_integration.report_generator import ReportGenerator
    
    correlator = CrossDomainCorrelator()
    predictor = CrossDomainPredictor(correlator=correlator)
    report_generator = ReportGenerator()
    
    system_integrator.register_component('correlator', correlator)
    system_integrator.register_component('predictor', predictor)
    system_integrator.register_component('report_generator', report_generator)
    
    return system_integrator