import datetime

class H2CertifyEngine:
    def __init__(self):
        # 2026 EU Statutory Fossil Comparator (94 gCO2e/MJ)
        self.FOSSIL_COMPARATOR = 94.0 
        self.GREEN_THRESHOLD = 28.2 # Max allowed (70% reduction)
        self.H2_LHV = 120.1 # Lower Heating Value of H2 (MJ/kg)

    def calculate_emissions(self, e_supply, e_process, e_transport):
        """
        Formula based on EU Delegated Act: E = e_i + e_p + e_td
        e_supply: Upstream emissions (Electricity/Feedstock)
        e_process: Electrolysis/Conversion emissions
        e_transport: Compression & Shipping
        """
        total_gco2_per_mj = e_supply + e_process + e_transport
        saving = (1 - (total_gco2_per_mj / self.FOSSIL_COMPARATOR)) * 100
        
        return {
            "total_intensity": round(total_gco2_per_mj, 2),
            "savings_percentage": round(saving, 2),
            "is_compliant": total_gco2_per_mj <= self.GREEN_THRESHOLD
        }

# --- EXAMPLE CASE: EXPORT FROM INDIA TO ESTONIA ---
# Data points for a 2026 shipment:
# 1. Supply (Renewable PPA + Grid): 5.0 gCO2e/MJ
# 2. Process (Efficiency losses): 8.5 gCO2e/MJ
# 3. Transport (Ammonia shipping to Tallinn): 10.2 gCO2e/MJ

engine = H2CertifyEngine()
shipment_report = engine.calculate_emissions(15.0, 8.5, 10.2)

print(f"--- H2-Certify Baltic: Compliance Report ---")
print(f"Intensity: {shipment_report['total_intensity']} gCO2e/MJ")
print(f"GHG Savings: {shipment_report['savings_percentage']}%")
print(f"EU RED III Status: {'CERTIFIED' if shipment_report['is_compliant'] else 'REJECTED'}")