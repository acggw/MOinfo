from classification_models.predict import predict_more_likely_than_p
from classification_models.models import bill_classificiation_tfidf_model
from config import POLICY_AREA_CERTAINTY


#Adds bill classes to sql_session
def classify_bill(sql_session, bill_version):
    policy_areas = predict_more_likely_than_p(bill_classificiation_tfidf_model, bill_version.text, p=POLICY_AREA_CERTAINTY)
    for policy_area in policy_areas:
        sql_session.add(
            bill_chamber = bill_version.bill_chamber,
            under = bill_version.under,
            bill_session = bill_version.bill_session,
            bill_id = bill_version.bill_id, 
            bill_version = bill_version.version,
            policy_area = policy_area,
            version = bill_version
        )
    return True