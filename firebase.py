from logging import warning
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import messaging
from pyfcm import FCMNotification
import os
import datetime

# Use a service account
cred_path = os.path.join(os.getcwd(),'gasos-30e82-firebase-adminsdk-8dpnz-d24215e4a8.json')
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)


db = firestore.client()


# def inputUser():
#     Manager_name = input("Manager를 입력하세요 : ")
#     Protected_name = input("Protected를 입력하세요 : ")
#     doc_ref = db.collection(u'Manager_%s'%Manager_name).document(u'Protected_%s'%Protected_name)
#     # print(f"해당 기기의 관리자는 {Manager_name}입니다.\n해당 기기의 피보호자는 {Protected_name}입니다.")
#     return Manager_name,Protected_name,doc_ref


def uploadState(path,COstate,LPGstate):

    testData = [{
                u'COstate': COstate,
                u'LPGstate': LPGstate,
                u"time":datetime.datetime.now()
            }]
    doc_ref = path
    doc_ref.update({
        u'stateLogList':firestore.ArrayUnion(testData)
        })

def sendMessage(Manager_name, errorMessage):

    APIKEY = 'AAAAGyC6vII:APA91bGaBncRUotTVyCve9EJKj4gCdi3uAM4gH6CWFnh11lt21LJWXkYSVXy5ISEaoRaBbd8mUTMfyTkk_uBaqgTWxbcG2g_RpLf9Q808mSlg6eI90QpVW8KIIrsQXNtPCLeKDt89R98'
    TOKEN = db.collection(u'Manager_%s'%Manager_name).document(u'FCM_Token').get().to_dict()['token']
    pushServer = FCMNotification(APIKEY)

    message = messaging.Message(
        notification= messaging.Notification(
            title = "warning",
            body = errorMessage,
            ),
        token=TOKEN,
    )

    response = messaging.send(message)
    print('Successfully sent message:', response)

# Manager, Protected, path= inputUser()
# uploadState(path,'양호','위험')
# sendMessage("대창너무조아",'CO가 위험수치 입니다.')


