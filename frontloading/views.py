from django.http.response import HttpResponseBadRequest
from django.shortcuts import redirect, render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.utils import timezone
from .render import Render
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.urls import reverse

from .models import *

wordTypes = ['verb', 'adj', 'noun']

def index(request):
    return render(request, 'frontloading/index.html')

def documents(request):
    query_set = {}
    dom = request.GET.get('domain')
    if dom:
        query_set['domains__name'] = request.GET.get('domain')
    topic = request.GET.get('topic')
    if topic:
        query_set['topics__name'] = request.GET.get('topic')

    context = {
        'document_list': Document.objects.filter(**query_set),
        'domains': Domain.objects.all(),
        'topics': Topic.objects.all()
    }
    return render(request, 'frontloading/document_list.html', context)

def update_document(doc: Document, title: str, words: str):
    doc.title = title
    idx = 0
    words = words.split(',')
    print(words)
    for i in range(5):
        if i < len(words) and len(words[i]) > 0:
            wd = Word.objects.get(id=int(words[i]))
            if wd:
                if idx == 0:
                    doc.word1 = wd
                elif idx == 1:
                    doc.word2 = wd
                elif idx == 2:
                    doc.word3 = wd
                elif idx == 3:
                    doc.word4 = wd
                elif idx == 4:
                    doc.word5 = wd
        else:
            # Empty word
            if idx == 0:
                doc.word1 = None
            elif idx == 1:
                doc.word2 = None
            elif idx == 2:
                doc.word3 = None
            elif idx == 3:
                doc.word4 = None
            elif idx == 4:
                doc.word5 = None
        idx = idx + 1
    
    doc.save()

def document(request, document_id = None):
    if request.method == 'POST':
        # Add
        print(request.POST)
        if len(request.POST.get('title')) == 0:
            return HttpResponseBadRequest()
        if len(request.POST.get('words')) == 0:
            return HttpResponseBadRequest()
        
        if request.POST.get('document_id'):
            doc = get_object_or_404(Document, id=document_id)
        else:
            # New
            doc = Document(
                create_date=timezone.now()
            )
        
        update_document(doc, request.POST.get('title'), request.POST.get('words'))
        return redirect('document-detail', document_id=doc.id)

    if document_id:
        return render(request, 'frontloading/document_detail.html', {
            'document': get_object_or_404(Document, id=document_id),
            'words': Word.objects.all()
        })
    else:
        return render(request, 'frontloading/document_detail.html', {
            'document': Document(),
            'words': Word.objects.all()
        })

def document_new(request):
    if request.method == 'POST':
        # Add
        print(request.POST)
        if len(request.POST.get('title')) == 0:
            return HttpResponseBadRequest()
        if len(request.POST.get('words')) == 0:
            return HttpResponseBadRequest()
        
        # Check for existing title
        doc_e = Document.objects.filter(title__startswith=request.POST.get('title'))
        print(doc_e)
        if doc_e:
            return HttpResponseBadRequest("Title already exists")

        doc = Document(
            create_date=timezone.now()
        )
        update_document(doc, request.POST.get('title'), request.POST.get('words'))
        return redirect('document-detail', document_id=doc.id)

    # List
    return render(request, 'frontloading/document_detail.html', {
        'document': Document(),
        'words': Word.objects.all()
    })

def domains(request):
    ''' Show or add/edit domain tags '''
    return render(request, 'frontloading/domains.html', {
        'domains': Domain.objects.all()
    })

def add_domain(_name):
    _name = _name.strip()
    dom_m = Domain.objects.filter(name__startswith=_name)
    if len(dom_m) > 0:
        # Exists
        print("Exists", _name)
        return None
    dom = Domain(
        name=_name,
        create_date=timezone.now()
    )
    dom.save()
    return dom

def add_topic(_name):
    _name = _name.strip()
    top_m = Topic.objects.filter(name__startswith=_name)
    if len(top_m) > 0:
        # Exists
        print("Exists", _name)
        return None
    top = Topic(
        name=_name,
        create_date=timezone.now()
    )
    top.save()
    return top

def domain_new(request):
    ''' Show or add/edit domain tags '''
    if request.method == 'POST':
        # Add
        print(request.POST)
        dom = add_domain(request.POST.get('name'))
        return redirect('domain-detail', domain_id=dom.id)

    return render(request, 'frontloading/domain_detail.html', {
        'domain': Domain()
    })

def domain(request, domain_id = None):
    ''' Show or add/edit domain tags '''
    domain = get_object_or_404(Domain, id=domain_id)
    if request.method == 'POST':
        # Edit
        if int(request.POST.get('id')) == domain_id:
            domain.name = request.POST.get('name')
            if len(domain.name) == 0:
                Domain.delete(domain)
            else:
                domain.save()

    return redirect('domains')
    # return render(request, 'frontloading/domain_detail.html', {
    #     'domain': domain
    # })

def topics(request):
    ''' Show or add/edit topics tags '''
    return render(request, 'frontloading/topics.html', {
        'topics': Topic.objects.all()
    })

def topic_new(request):
    ''' Show or add/edit topics tags '''
    if request.method == 'POST':
        # Add
        dom = add_topic(request.POST.get('name'))
        return redirect('topic-detail', topic_id=dom.id)

    return render(request, 'frontloading/topics_detail.html', {
        'topic': Topic()
    })

def topic(request, topic_id = None):
    ''' Show or add/edit topics tags '''
    topic = get_object_or_404(Topic, id=topic_id)
    if request.method == 'POST':
        # Edit
        if int(request.POST.get('id')) == topic_id:
            topic.name = request.POST.get('name')
            if len(topic.name) == 0:
                Topic.delete(topic)
            else:
                topic.save()

    return redirect('topics')

def word_new(request):
    ''' Show or add/edit vocab word '''
    if request.method == 'POST':
        # Add
        print(request.POST)
        
        word = Word(
            create_date=timezone.now()
        )
        word.name = request.POST.get('name').lower()
        if request.POST.get('type') in wordTypes:
            word.type = request.POST.get('type')
        word.pronunciation = request.POST.get('pronunciation')
        word.parts = request.POST.get('parts')
        word.etymology = request.POST.get('etymology')
        word.definition = request.POST.get('definition')
        word.word_family = request.POST.get('family')
        word.synonyms = request.POST.get('synonyms')
        word.example = request.POST.get('example')
        word.sentence = request.POST.get('sentence')

        if 'image' in request.FILES:
            word.image = request.FILES['image']
        
        word.save()

        domains_text = request.POST.get('domains').split(',')
        for dom in domains_text:
            dom = dom.strip()
            if len(dom) == 0:
                continue
            dom_m = Domain.objects.filter(name__startswith=dom)
            if len(dom_m) > 0:
                word.domains.add(dom_m[0])
            else:
                dom_n = add_domain(dom)
                if dom_n:
                    word.domains.add(dom_n)
        topic_text = request.POST.get('topics').split(',')
        for dom in topic_text:
            dom = dom.strip()
            if len(dom) == 0:
                continue
            dom_m = Topic.objects.filter(name__startswith=dom)
            if len(dom_m) > 0:
                word.topics.add(dom_m[0])
            else:
                dom_n = add_topic(dom)
                if dom_n:
                    word.topics.add(dom_n)

        word.save()
        if request.POST.get('button') == "sub_new":
            return HttpResponse(reverse('word-new'))
        else:
            return HttpResponse(reverse('word-detail', args=[word.id]))

    # List
    return render(request, 'frontloading/word_detail.html', {
        'word': Word(),
        'types': wordTypes,
        'domains': Domain.objects.all(),
        'topics': Topic.objects.all()
    })

def word(request, word_id = None):
    ''' Show or add/edit domain tags '''
    word = get_object_or_404(Word, id=word_id)
    if request.method == 'POST':
        # Edit
        if int(request.POST.get('id')) == word_id:
            print(request.POST)
            word.name = request.POST.get('name').lower()
            if request.POST.get('type') in wordTypes:
                word.type = request.POST.get('type')
            word.pronunciation = request.POST.get('pronunciation')
            word.parts = request.POST.get('parts')
            word.etymology = request.POST.get('etymology')
            word.definition = request.POST.get('definition')
            word.word_family = request.POST.get('family')
            word.synonyms = request.POST.get('synonyms')
            word.example = request.POST.get('example')
            word.sentence = request.POST.get('sentence')

            if 'image' in request.FILES:
                word.image = request.FILES['image']

            word.domains.clear()
            word.topics.clear()
            domains_text = request.POST.get('domains').split(',')
            for dom in domains_text:
                dom = dom.strip()
                if len(dom) == 0:
                    continue
                dom_m = Domain.objects.filter(name__startswith=dom)
                if len(dom_m) > 0:
                    word.domains.add(dom_m[0])
                else:
                    dom_n = add_domain(dom)
                    if dom_n:
                        word.domains.add(dom_n)
            topic_text = request.POST.get('topics').split(',')
            for dom in topic_text:
                dom = dom.strip()
                if len(dom) == 0:
                    continue
                dom_m = Topic.objects.filter(name__startswith=dom)
                if len(dom_m) > 0:
                    word.topics.add(dom_m[0])
                else:
                    dom_n = add_topic(dom)
                    if dom_n:
                        word.topics.add(dom_n)
            word.save()

            return HttpResponse(reverse('word-detail', args=[word.id]))

    return render(request, 'frontloading/word_detail.html', {
        'word': word,
        'types': wordTypes,
        'domains': Domain.objects.all(),
        'topics': Topic.objects.all()
    })

def words(request):
    ''' Show words '''
    query_set = {}
    dom = request.GET.get('domain')
    if dom:
        query_set['domains__name'] = request.GET.get('domain')
    topic = request.GET.get('topic')
    if topic:
        query_set['topics__name'] = request.GET.get('topic')
    
    return render(request, 'frontloading/word_list.html', {
        'words': Word.objects.all().filter(**query_set).order_by('name'),
        'domains': Domain.objects.all(),
        'topics': Topic.objects.all()
    })



@xframe_options_sameorigin
def document_pdf(request, document_id):
    doc = get_object_or_404(Document, id=document_id)
    return Render.render('frontloading/document_pdf.html', {
        "document": doc,
        "bandw": bw == 'true'
    })

@xframe_options_sameorigin
def document_prieview(request, document_id):
    doc = get_object_or_404(Document, id=document_id)
    bw = request.GET.get('bandw', '')
    print(bw)
    return render(request, 'frontloading/document_pdf.html', {
        "document": doc,
        "bandw": bw == 'true'
    })

# def picture_upload(request):
#     ''' Handle new image upload '''
#     if 'image' in request.FILES:
#         pic = Picture()
#         pic.image = request.FILES['image']
#         pic.save()
#         return HttpResponse(f'<img src="{pic.image.url}" >')
#     return HttpResponseBadRequest("no file in request")

# def picture_get(request, picture_id):
#     pic = get_object_or_404(Picture, id=picture_id)
#     return HttpResponse(f'<img src="{pic.image.url}" >') # ToDo

def words_backup(request):
    from django.core import serializers
    data = serializers.serialize("json", Word.objects.all())
    data += serializers.serialize("json", Document.objects.all())
    data += serializers.serialize("json", Domain.objects.all())
    data += serializers.serialize("json", Topic.objects.all())
    data += serializers.serialize("json", VocBank.objects.all())
    return HttpResponse(data, content_type="aplication/json")

### Vocbulary Banks 
###

def banks(request):
    query_set = {}
    dom = request.GET.get('domain')
    if dom:
        query_set['domains__name'] = request.GET.get('domain')
    
    context = {
        'bank_list': VocBank.objects.filter(**query_set).order_by('title'),
        'domains': Domain.objects.all()
    }
    return render(request, 'frontloading/bank_list.html', context)

def get_item(list, idx, default=''):
    if idx < len(list):
        return list[idx]
    else:
        return default

def bank(request, bank_id = None):
    if request.method == 'POST':
        # Add
        if len(request.POST.get('title')) == 0:
            return HttpResponseBadRequest()
        print(bank_id, request.POST.get('bank_id'))
        if request.POST.get('bank_id') and bank_id:
            bank = get_object_or_404(VocBank, id=bank_id)
        else:
            # New
            bank = VocBank(
                create_date=timezone.now()
            )
        
        bank.title = request.POST.get('title')
        bank.disciplinary_year7 = request.POST.get('disc_y7', '')
        bank.disciplinary_year8 = request.POST.get('disc_y8', '')
        bank.disciplinary_year9 = request.POST.get('disc_y9', '')
        bank.disciplinary_year10 = request.POST.get('disc_y10', '')

        bank.task_year7 = request.POST.get('task_y7', '')
        bank.task_year8 = request.POST.get('task_y8', '')
        bank.task_year9 = request.POST.get('task_y9', '')
        bank.task_year10 = request.POST.get('task_y10', '')
        
        bank.academic_vocab = request.POST.get('academic_vocab', '')
        bank.save()

        domains_text = request.POST.get('domains').split(',')
        for dom in domains_text:
            dom = dom.strip()
            if len(dom) == 0:
                continue
            dom_m = Domain.objects.filter(name__startswith=dom)
            if len(dom_m) > 0:
                bank.domains.add(dom_m[0])
            else:
                dom_n = add_domain(dom)
                if dom_n:
                    bank.domains.add(dom_n)
        bank.save()
        
        return redirect('bank-detail', bank_id=bank.id)

    if bank_id:
        return render(request, 'frontloading/bank_detail.html', {
            'bank': get_object_or_404(VocBank, id=bank_id)
        })
    else:
        return render(request, 'frontloading/bank_detail.html', {
            'bank': VocBank()
        })

def bank_new(request):
    b = VocBank()
    b.id = 0
    return render(request, 'frontloading/bank_detail.html', {
        'bank': b
    })

@xframe_options_sameorigin
def bank_prieview(request, bank_id):
    bw = request.GET.get('bandw', '')
    
    bank = get_object_or_404(VocBank, id=bank_id)

    d7list = [x for x in bank.disciplinary_year7.split(',') if x]
    d8list = [x for x in bank.disciplinary_year8.split(',') if x]
    d9list = [x for x in bank.disciplinary_year9.split(',') if x]
    d10list = [x for x in bank.disciplinary_year10.split(',') if x]

    discLen = len(d7list)
    if len(d8list) > discLen:
        discLen = len(d8list)
    if len(d9list) > discLen:
        discLen = len(d9list)
    if len(d10list) > discLen:
        discLen = len(d10list)
    discLen = (discLen // 2) + 1
    # Build combined list of words for table rows
    # y7, y7, y8, y8, y9, y9, y10, y10
    y7idx = 0
    y8idx = 0
    y9idx = 0
    y10idx = 0
    disc_word = []
    for i in range(discLen):
        row = []
        row.append(get_item(d7list, y7idx))
        row.append(get_item(d7list, y7idx+1))
        y7idx=y7idx+2
        row.append(get_item(d8list, y8idx))
        row.append(get_item(d8list, y8idx+1))
        y8idx=y8idx+2
        row.append(get_item(d9list, y9idx))
        row.append(get_item(d9list, y9idx+1))
        y9idx=y9idx+2
        row.append(get_item(d10list, y10idx))
        row.append(get_item(d10list, y10idx+1))
        y10idx=y10idx+2
        disc_word.append(row)
    
    d7list = [x for x in bank.task_year7.split(',') if x]
    d8list = [x for x in bank.task_year8.split(',') if x]
    d9list = [x for x in bank.task_year9.split(',') if x]
    d10list = [x for x in bank.task_year10.split(',') if x]

    discLen = len(d7list)
    if len(d8list) > discLen:
        discLen = len(d8list)
    if len(d9list) > discLen:
        discLen = len(d9list)
    if len(d10list) > discLen:
        discLen = len(d10list)
    discLen = (discLen // 2) + 1
    # Build combined list of words for table rows
    # y7, y7, y8, y8, y9, y9, y10, y10
    y7idx = 0
    y8idx = 0
    y9idx = 0
    y10idx = 0
    task_word = []
    for i in range(discLen):
        row = []
        row.append(get_item(d7list, y7idx))
        row.append(get_item(d7list, y7idx+1))
        y7idx=y7idx+2
        row.append(get_item(d8list, y8idx))
        row.append(get_item(d8list, y8idx+1))
        y8idx=y8idx+2
        row.append(get_item(d9list, y9idx))
        row.append(get_item(d9list, y9idx+1))
        y9idx=y9idx+2
        row.append(get_item(d10list, y10idx))
        row.append(get_item(d10list, y10idx+1))
        y10idx=y10idx+2
        task_word.append(row)

    acad_words = [x for x in bank.academic_vocab.split(',') if x]
    for i in range(len(acad_words), 24):
        acad_words.append(" ")

    return render(request, 'frontloading/bank_pdf.html', {
        "bank": bank,
        "bandw": bw == 'true',
        "disc_words": disc_word,
        "task_words" : task_word,
        "acad_words": acad_words
    })
