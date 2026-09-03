with open('index.html', encoding='utf-8') as f:
    html = f.read()

OLD_KPI = """const KPI_BY_CONTRACT = {
  'Impulse & Grocery': [
    { label: 'Availability',   comp: 'avail_compliance',           inc: 'avail_incentive' },
    { label: 'Share of Shelf', comp: 'sos_compliance',             inc: 'sos_incentive' },
    { label: 'Strike Zone',    comp: 'sz_compliance',              inc: 'sz_incentive' },
    { label: 'Large Cooler',   comp: 'large_cooler_compliance',    inc: 'large_cooler_incentive' },
  ],
  'Supermarket': [
    { label: 'Availability',      comp: 'avail_compliance',          inc: 'avail_incentive' },
    { label: 'Share of Shelf',    comp: 'sos_compliance',            inc: 'sos_incentive' },
    { label: 'Strike Zone',       comp: 'sz_compliance',             inc: 'sz_incentive' },
    { label: 'Price',             comp: 'price_compliance',          inc: 'price_incentive' },
    { label: 'POSM',              comp: 'posm_compliance',           inc: 'posm_incentive' },
    { label: 'Ambient Placement', comp: 'ambient_compliance',        inc: 'ambient_incentive' },
    { label: 'Cooler @ Cashier',  comp: 'cooler_cashier_compliance', inc: 'cooler_cashier_incentive' },
  ],
  'Gas Station': [
    { label: 'Availability',      comp: 'avail_compliance',             inc: 'avail_incentive' },
    { label: 'Share of Shelf',    comp: 'sos_compliance',               inc: 'sos_incentive' },
    { label: 'Strike Zone',       comp: 'sz_compliance',                inc: 'sz_incentive' },
    { label: 'Price',             comp: 'price_compliance',             inc: 'price_incentive' },
    { label: 'Sticky Shelf',      comp: 'sticky_compliance',            inc: 'sticky_incentive' },
    { label: 'Chilled 2m Cashier',comp: 'chilled_cashier_compliance',   inc: 'chilled_cashier_incentive' },
  ],
  'Bazar': [
    { label: 'Availability',         comp: 'avail_compliance',          inc: 'avail_incentive' },
    { label: 'Share of Shelf',       comp: 'sos_compliance',            inc: 'sos_incentive' },
    { label: 'Strike Zone',          comp: 'sz_compliance',             inc: 'sz_incentive' },
    { label: 'Outdoor Visibility',   comp: 'outdoor_compliance',        inc: 'outdoor_incentive' },
    { label: 'POSM',                 comp: 'posm_compliance',           inc: 'posm_incentive' },
    { label: 'Cooler Accessible',    comp: 'cooler_visible_compliance',  inc: 'cooler_visible_incentive' },
  ],
};"""

NEW_KPI = """const KPI_BY_CONTRACT = {
  'Impulse & Grocery': [
    { label: 'Availability',   comp: 'avail_compliance',           inc: 'avail_incentive' },
    { label: 'Share of Shelf', comp: 'sos_compliance',             inc: 'sos_incentive' },
    { label: 'Strike Zone',    comp: 'sz_compliance',              inc: 'sz_incentive' },
    { label: 'Large Cooler',   comp: 'large_cooler_compliance',    inc: 'large_cooler_incentive' },
  ],
  'Supermarket': [
    { label: 'Availability',      comp: 'avail_compliance',          inc: 'avail_incentive' },
    { label: 'Share of Shelf',    comp: 'sos_compliance',            inc: 'sos_incentive' },
    { label: 'Strike Zone',       comp: 'sz_compliance',             inc: 'sz_incentive' },
    { label: 'Price',             comp: 'price_compliance',          inc: 'price_incentive' },
    { label: 'Ambient Placement', comp: 'ambient_compliance',        inc: 'ambient_incentive' },
    { label: 'Cooler @ Cashier',  comp: 'cooler_cashier_compliance', inc: 'cooler_cashier_incentive' },
  ],
  'Gas Station': [
    { label: 'Availability',            comp: 'avail_compliance',           inc: 'avail_incentive' },
    { label: 'Share of Shelf',          comp: 'sos_compliance',             inc: 'sos_incentive' },
    { label: 'Strike Zone',             comp: 'sz_compliance',              inc: 'sz_incentive' },
    { label: 'Price',                   comp: 'price_compliance',           inc: 'price_incentive' },
    { label: 'Sticky Shelf',            comp: 'sticky_compliance',          inc: 'sticky_incentive' },
    { label: 'Chilled 2m Cashier',      comp: 'chilled_cashier_compliance', inc: 'chilled_cashier_incentive' },
    { label: 'Brand Visibility / Msg',  comp: 'posm_compliance',            inc: 'posm_incentive' },
  ],
  'Bazar': [
    { label: 'Availability',       comp: 'avail_compliance',          inc: 'avail_incentive' },
    { label: 'Outdoor Visibility', comp: 'outdoor_compliance',        inc: 'outdoor_incentive' },
    { label: 'Pricing',            comp: 'price_compliance',          inc: 'price_incentive' },
    { label: 'Cooler Accessible',  comp: 'cooler_visible_compliance', inc: 'cooler_visible_incentive' },
  ],
};"""

if OLD_KPI in html:
    html = html.replace(OLD_KPI, NEW_KPI)
    print("KPI mappings updated successfully")
else:
    print("ERROR: target not found")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
