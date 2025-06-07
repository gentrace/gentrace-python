"""Example workflow that will be auto-traced with pipeline_id."""

import time
from typing import Any, Dict, List

import gentrace


def run_data_processing_pipeline() -> Dict[str, Any]:
    """Main pipeline entry point - this and all called functions will have pipeline_id."""
    print("Starting data processing pipeline...")
    
    # Step 1: Extract data
    print("Step 1: Extracting data...")
    data = extract_data()
    print(f"  Extracted {len(data)} records")
    
    # Step 2: Transform data
    print("Step 2: Transforming data...")
    transformed = transform_data(data)
    print(f"  Transformed {len(transformed)} records")
    
    # Step 3: Load results
    print("Step 3: Loading results...")
    result = load_results(transformed)
    print("  Results loaded successfully")
    
    return result


def extract_data() -> List[Dict[str, Any]]:
    """Extract data from source."""
    time.sleep(0.05)  # Simulate work
    
    # Simulate extracting data
    data: List[Dict[str, Any]] = []
    for i in range(5):  # Reduced for faster example
        record = process_record(i)
        data.append(record)
    
    return data


def process_record(record_id: int) -> Dict[str, Any]:
    """Process individual record."""
    # This will also be traced with the pipeline_id
    return {
        'id': record_id,
        'value': record_id * 10,
        'status': 'extracted'
    }


def transform_data(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Transform the extracted data."""
    transformed: List[Dict[str, Any]] = []
    for record in data:
        # Apply transformation
        result = apply_transformation(record)
        if validate_transformation(result):
            transformed.append(result)
    
    return transformed


def apply_transformation(record: Dict[str, Any]) -> Dict[str, Any]:
    """Apply transformation to a single record."""
    time.sleep(0.01)  # Simulate work
    
    return {
        **record,
        'value': record['value'] * 2,
        'status': 'transformed',
        'transform_timestamp': time.time()
    }


def validate_transformation(record: Dict[str, Any]) -> bool:
    """Validate the transformed record."""
    return record.get('value', 0) > 0 and 'transform_timestamp' in record


def load_results(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Load the results to destination."""
    time.sleep(0.05)  # Simulate work
    
    # Generate summary with auto-tracing
    summary = generate_summary(data)
    
    # Also demonstrate manual tracing within auto-traced code
    enriched_summary = enrich_summary_manually(summary)
    
    return {
        'status': 'success',
        'records_processed': len(data),
        'summary': enriched_summary,
        'pipeline_complete': True
    }


@gentrace.no_auto_trace  # Exclude from auto-tracing
def enrich_summary_manually(summary: Dict[str, Any]) -> Dict[str, Any]:
    """Function that uses @traced decorator for manual tracing."""
    # Use the traced decorator directly
    @gentrace.traced(
        name="Manual Summary Enrichment", 
        attributes={"custom_attribute": "manual_trace", "enrichment_type": "statistics"}
    )
    def _enrich() -> Dict[str, Any]:
        time.sleep(0.01)  # Simulate work
        return {
            **summary,
            'enriched': True,
            'percentile_95': summary.get('average', 0) * 1.5 if summary else 0,
            'traced_manually': True
        }

    return _enrich()


def generate_summary(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate summary statistics (auto-traced)."""
    if not data:
        return {'total': 0, 'average': 0}
    
    values = [r.get('value', 0) for r in data]
    
    # Add a small simulated calculation
    time.sleep(0.02)  # Simulate computation time
    
    return {
        'total': sum(values),
        'average': sum(values) / len(values),
        'count': len(data),
        'interaction_wrapped': True  # Marker to show this was wrapped
    }