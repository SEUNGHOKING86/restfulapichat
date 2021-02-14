from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Addresses
from .serializers import AddressesSerializer
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json
import numpy as np
import random
import colorama

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder


# Create your views here.


def home(request):
    context = {}

    return render(request, "chatbot/chathome.html", context)


@csrf_exempt
def chattrain(request):
    context = {}

    # file = open(f"{CURRENT_WORKING_DIRECTORY}intents.json", encoding="UTF-8")
    file = open(f"./static/intents.json", encoding="UTF-8")
 #   data = json.loads(file.read())
    data = json.loads(file.read())

    # js = json.loads(data.decode("utf-8"))

    training_sentences = []
    training_labels = []
    labels = []
    responses = []

    for intent in data['intents']:
        for pattern in intent['patterns']:
            training_sentences.append(pattern)
            training_labels.append(intent['tag'])
        responses.append(intent['responses'])

        if intent['tag'] not in labels:
            labels.append(intent['tag'])

    num_classes = len(labels)

    lbl_encoder = LabelEncoder()
    lbl_encoder.fit(training_labels)
    training_labels = lbl_encoder.transform(training_labels)

    vocab_size = 1000
    embedding_dim = 16
    max_len = 20
    oov_token = "<OOV>"

    tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_token)
    tokenizer.fit_on_texts(training_sentences)
    word_index = tokenizer.word_index
    sequences = tokenizer.texts_to_sequences(training_sentences)
    padded_sequences = pad_sequences(sequences, truncating='post', maxlen=max_len)

    # Model Training

    model = Sequential()
    model.add(Embedding(vocab_size, embedding_dim, input_length=max_len))
    model.add(GlobalAveragePooling1D())
    model.add(Dense(16, activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))

    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer='adam', metrics=['accuracy'])

    model.summary()

    epochs = 500
    history = model.fit(padded_sequences, np.array(training_labels), epochs=epochs)

    # to save the trained model
    model.save("static/chat_model")

    import pickle

    # to save the fitted tokenizer
    with open('static/tokenizer.pickle', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # to save the fitted label encoder
    with open('static/label_encoder.pickle', 'wb') as ecn_file:
        pickle.dump(lbl_encoder, ecn_file, protocol=pickle.HIGHEST_PROTOCOL)

    context['result'] = 'Success'

    return JsonResponse(context, content_type="application/json")


@csrf_exempt
def chatanswer(request):
    context = {}

    inp = request.GET['chattext']

    import colorama
    colorama.init()
    from colorama import Fore, Style, Back

    import random
    import pickle

    file = open(f"./static/intents.json", encoding="UTF-8")
    data = json.load(file)

    model = keras.models.load_model('static/chat_model')

    # load tokenizer object
    with open('static/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    # load label encoder object
    with open('static/label_encoder.pickle', 'rb') as enc:
        lbl_encoder = pickle.load(enc)

    # parameters
    max_len = 20

    print(Fore.LIGHTBLUE_EX + "User: " + Style.RESET_ALL, end="")

    result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]),
                                                                      truncating='post', maxlen=max_len))
    tag = lbl_encoder.inverse_transform([np.argmax(result)])

    for i in data['intents']:
        if i['tag'] == tag:
            text1 = np.random.choice(i['responses'])
            print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL, text1)

    context["anstext"] = text1

    return JsonResponse(context, content_type="application/json")



@csrf_exempt
def address_list(request):
    if request.method == 'GET':
        query_set = Addresses.objects.all()
        serializer = AddressesSerializer(query_set, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AddressesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def address(request, pk):

    obj = Addresses.objects.get(pk=pk)

    if request.method == 'GET':
        serializer = AddressesSerializer(obj)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = AddressesSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        obj.delete()
        return HttpResponse(status=204)


# @csrf_exempt
# def login(request):
#     if request.method == 'POST':
#         data = JSONParser().parse(request)
#         search_name = data['name']
#         obj = Addresses.objects.get(name=search_name)
#
#         if data['phone_number'] == obj.phone_number:
#             return HttpResponse(status=200)
#         else:
#             return HttpResponse(status=400)


@csrf_exempt
def login(request):

    if request.method == 'POST':

        print("리퀘스트 로그" + str(request))
        print("리퀘스트 로그" + str(request.body))
        userid = request.POST.get('userid', '')
        userpw = request.POST.get('userpw', '')
        result = authenticate(username=userid, password=userpw)

        print("id = " + userid + " userpw = " + userpw)

        # if result :
        #
        #     return HttpResponse(status=200)
        # else:
        #     return HttpResponse(status=401)


    return HttpResponse(status=200)

@csrf_exempt
def login_page(request):
    return render(request, "chatbot/login.html")
    # if request.method == 'POST':
    #
    #     print("리퀘스트 로그" + str(request))
    #     print("리퀘스트 바디" + str(request.body))
    #     userid = request.POST.get('userid', '')
    #     userpw = request.POST.get('userpw', '')
    #     result = authenticate(username=userid, password=userpw)
    #
    #     print("id = " + userid + " result = " + str(login_result))
    #
    #     if login_result:
    #         return HttpResponse(status=200)
    #     else:
    #         return render(request, "chatbot/login.html", status=401)



    #     result = authenticate(username=id, password=pw)
    #
    #     if result :
    #         print("로그인 성공!")
    #         return HttpResponse(status=200)
    #     else:
    #         print("실패")
    #         return HttpResponse(status=401)
    #         return HttpResponse(status=401)


@csrf_exempt
def app_login(request):

    if request.method == 'POST':
        print("리퀘스트 로그" + str(request.body))
        id = request.POST.get('userid', '')
        pw = request.POST.get('userpw', '')
        print("id = " + id + " pw = " + pw)

        result = authenticate(username=id, password=pw)

        if result:
            print("로그인 성공!")
            return JsonResponse({'code': '0000', 'msg': '로그인성공입니다.'}, status=200)
        else:
            print("실패")
            return JsonResponse({'code': '1001', 'msg': '로그인실패입니다.'}, status=200)


@csrf_exempt
def chat_service(request):
    if request.method == 'POST':
        input1 = request.POST['input1']
        print(input1)
        output = dict()
        output['response'] = "이건 응답"
        return HttpResponse(json.dumps(output), status=200)
    else:
        return render(request, 'addresses/chat_t:wqest.html')