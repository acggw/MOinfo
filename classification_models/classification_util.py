from classification_models.predict import predict_areas
from database.tables.bills import Bill_Policy_Area

#Adds bill classes to sql_session
def classify_bill(sql_session, bill_version):
    policy_areas = predict_areas(bill_version.text)
    if len(policy_areas) == 0:
        print("No policy areas identified")
    for policy_area in policy_areas:
        sql_session.add(Bill_Policy_Area(
            bill_chamber = bill_version.bill_chamber,
            under = bill_version.under,
            bill_session = bill_version.bill_session,
            bill_id = bill_version.bill_id, 
            bill_version = bill_version.version,
            policy_area = policy_area,
            version = bill_version
        )
        )
    return True