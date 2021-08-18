from django.db import models


class Domain(models.Model):
    name = models.CharField(max_length=100)
    create_date = models.DateTimeField('date created')    

class Subject(models.Model):
    name = models.CharField(max_length=100)
    create_date = models.DateTimeField('date created')

class Topic(models.Model):
    name = models.CharField(max_length=100)
    create_date = models.DateTimeField('date created')

class Tag(models.Model):
    name = models.CharField(max_length=100)
    create_by = models.CharField(max_length=100)
    create_date = models.DateTimeField('date created')

class Definition(models.Model):
    name = models.CharField(max_length=100)


class Word(models.Model):
    name = models.CharField(max_length=100) # Vocab..
    type = models.CharField(max_length=100) # noun, verb, etc.
    pronunciation = models.CharField(max_length=200)
    parts = models.CharField(max_length=200, default="")
    etymology = models.CharField(max_length=200, default="")
    definition = models.CharField(max_length=300)
    word_family = models.CharField(max_length=200)
    image = models.ImageField(null=True, default=None)
    synonyms = models.CharField(max_length=200)
    example = models.CharField(max_length=500)
    sentence = models.CharField(max_length=500)

    domains = models.ManyToManyField(Domain)
    topics = models.ManyToManyField(Topic)
    tags = models.CharField(max_length=200)
    
    create_date = models.DateTimeField('date created')

    def word_family_as_list(self):
        return [x for x in self.word_family.split(',') if x]
    
    def synonyms_as_list(self):
        return [x for x in self.synonyms.split(',') if x]
    
    def parts_as_list(self):
        return [x for x in self.parts.split('\n') if x]

class Document(models.Model):
    ''' Represents an already built fronloading document '''
    title = models.CharField(max_length=200)
    # content_reference = models.CharField(max_length=100)
    word1 = models.ForeignKey(Word, null=True, default=None, on_delete=models.RESTRICT, related_name="word1")
    word2 = models.ForeignKey(Word, null=True, default=None, on_delete=models.RESTRICT, related_name="word2")
    word3 = models.ForeignKey(Word, null=True, default=None, on_delete=models.RESTRICT, related_name="word3")
    word4 = models.ForeignKey(Word, null=True, default=None, on_delete=models.RESTRICT, related_name="word4")
    word5 = models.ForeignKey(Word, null=True, default=None, on_delete=models.RESTRICT, related_name="word5")

    domains = models.ManyToManyField(Domain)
    topics = models.ManyToManyField(Topic)
    tags = models.CharField(max_length=200)
    
    create_date = models.DateTimeField('date created')

class VocBank(models.Model):
    ''' Represents vocabulary bank document '''
    title = models.CharField(max_length=200)
    # content_reference = models.CharField(max_length=100)
    disciplinary_year7 = models.CharField(max_length=500)
    disciplinary_year8 = models.CharField(max_length=500)
    disciplinary_year9 = models.CharField(max_length=500)
    disciplinary_year10 = models.CharField(max_length=500)
    
    task_year7 = models.CharField(max_length=200)
    task_year8 = models.CharField(max_length=200)
    task_year9 = models.CharField(max_length=200)
    task_year10 = models.CharField(max_length=200)
    
    academic_vocab = models.CharField(max_length=600)

    domains = models.ManyToManyField(Domain)
    
    create_date = models.DateTimeField('date created')

    def disc_y7_list(self):
        return [x for x in self.disciplinary_year7.split(',') if x]
    def disc_y8_list(self):
        return [x for x in self.disciplinary_year8.split(',') if x]
    def disc_y9_list(self):
        return [x for x in self.disciplinary_year9.split(',') if x]
    def disc_y10_list(self):
        return [x for x in self.disciplinary_year10.split(',') if x]

    def task_y7_list(self):
        return [x for x in self.task_year7.split(',') if x]
    def task_y8_list(self):
        return [x for x in self.task_year8.split(',') if x]
    def task_y9_list(self):
        return [x for x in self.task_year9.split(',') if x]
    def task_y10_list(self):
        return [x for x in self.task_year10.split(',') if x]
    
    def academic_vocab_list(self):
        return [x for x in self.academic_vocab.split(',') if x]


class User(models.Model):
    name = models.CharField(max_length=100)
    oauth_ident = models.CharField(max_length=100)
    last_online = models.DateTimeField('date modified')
    create_date = models.DateTimeField('date created')