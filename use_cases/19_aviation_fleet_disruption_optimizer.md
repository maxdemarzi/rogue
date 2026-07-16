# ✈️ Use Case 19: Aviation Fleet Disruption & Route Capacity Optimizer

This playbook implements the **Aviation Fleet Disruption & Route Capacity Optimizer**—a sector-specialty investment and operational risk modeling workflow. It models passenger traffic load factors, route performance margins, and fleet delivery delays to project operational distress for airlines.

---

## 🎯 The Mind-Blowing Analyst Capabilities
* **Fleet Order Bottleneck Tracing:** Simulates how manufacturing delivery delays affect passenger carrying capacities and load factors.
* **Safety Incident Volatility Shocks:** Simulates passenger load factor decay around major safety incident disclosures.
* **Route Margin Degradation Projections:** Projects route-by-route operating margin reductions used to screen sector acquisition targets.

---

## 🛠️ Datasets Utilized in this Workspace
1. **[data/aviation_industry/](file:///home/maxdemarzi/rogue/data/aviation_industry/)**: Fleet orders, route metrics, passenger traffic, and incidents.
2. **[data/fundamentals/](file:///home/maxdemarzi/rogue/data/fundamentals/)**: Operating expenses and capital returns.

---

## 🔗 Knowledge Graph Resolution Paths

### 1. Route Disruption Mapping
Link routes and aircraft orders to airline performance:
```
(:Company {name: $AIRLINE}) -[:OPERATES]-> (:RoutePerformance {route_name: $ROUTE, operating_margin: $MARGIN})
  <-[:ORDERED_BY]- (:FleetOrder {aircraft_type: $AIRCRAFT, delivery_status: $STATUS})
```

---

## 💻 Technical Solution Steps

### Step 1: Trace Fleet Delivery Delays
Identify delayed aircraft deliveries:
```python
import pandas as pd

fleet_df = pd.read_csv('data/aviation_industry/fleet_orders.csv')
delayed_orders = fleet_df[fleet_df['delivery_status'] == 'Delayed']

print("=== DELAYED FLEET ORDERS ===")
print(delayed_orders[['airline', 'aircraft_type', 'quantity', 'order_year']])
```
