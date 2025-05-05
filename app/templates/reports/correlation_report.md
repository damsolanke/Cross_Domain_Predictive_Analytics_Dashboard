# {{ title }}

*Generated at: {{ generated_at | format_date }}*

Report period: {{ start_date | format_date("%Y-%m-%d") }} to {{ end_date | format_date("%Y-%m-%d") }}

## Summary

This report analyzes correlations between different data domains and presents key insights derived from these correlations.

### Key Statistics

- **Total Insights:** {{ summary.total_insights }}
- **Strong Correlations:** {{ summary.strong_correlations }}
- **Domain Pairs:** {{ summary.domain_pairs | length }}

{% if summary.most_significant_insight %}
### Most Significant Insight

**{{ summary.most_significant_insight.domain1 | upper }} ↔ {{ summary.most_significant_insight.domain2 | upper }}**

{{ summary.most_significant_insight.description }}

Correlation: {{ summary.most_significant_insight.correlation_value | format_number }}
{% endif %}

## Correlation Analysis

{% if correlations.heatmap_data %}
The correlation analysis examined relationships between variables across different domains. The strongest correlations were observed between:

{% for dataset in correlations.heatmap_data %}
{% for item in dataset.data %}
{% if item.value | abs > 0.7 %}
- **{{ item.x }}** and **{{ item.y }}**: {{ item.value | format_number }}
{% endif %}
{% endfor %}
{% endfor %}
{% endif %}

## Top Insights

{% if insights %}
{% for insight in insights[:5] %}
### {{ insight.domain1 | upper }} ↔ {{ insight.domain2 | upper }}

{{ insight.description }}

- **Variables:** {{ insight.variable1 }} and {{ insight.variable2 }}
- **Correlation:** {{ insight.correlation_value | format_number }}
- **Detected:** {{ insight.timestamp | format_date }}

{% endfor %}

{% if insights | length > 5 %}
*Showing 5 of {{ insights | length }} insights.*
{% endif %}
{% else %}
No insights available for the selected period.
{% endif %}

{% if predictions %}
## Related Predictions

The following predictions were made based on correlation patterns:

{% for prediction in predictions[:3] %}
### {{ prediction.target_domain | title }}: {{ prediction.target_variable }}

- **Prediction:** {{ prediction.prediction | format_number }}
- **Confidence:** {{ (prediction.confidence * 100) | format_number }}%
- **Time:** {{ prediction.timestamp | format_date }}

{% endfor %}

{% if predictions | length > 3 %}
*Showing 3 of {{ predictions | length }} predictions.*
{% endif %}
{% endif %}

## Conclusions

The correlation analysis reveals significant relationships between variables across different domains. These insights can be used to improve prediction accuracy and understand the interconnected nature of the system.

---

*Cross-Domain Predictive Analytics Dashboard*

*Report generated using automated correlation analysis*