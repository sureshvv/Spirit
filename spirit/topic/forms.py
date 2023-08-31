# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import smart_bytes
from django.utils import timezone
from django.contrib.auth import get_user_model

from ..core import utils
from ..core.utils.forms import NestedModelChoiceField
from ..category.models import Category
from .models import Topic

from taggit.forms import TagField
from taggit_labels.widgets import LabelWidget

User = get_user_model()


class TopicForm(forms.ModelForm):

    topic_hash = forms.CharField(
        max_length=32,
        widget=forms.HiddenInput,
        required=False)
    tags = TagField(required=False, widget=LabelWidget)

    class Meta:
        model = Topic
        fields = ('title', 'category', 'assignee', 'tags')

    def __init__(self, user, *args, **kwargs):
        super(TopicForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['category'] = NestedModelChoiceField(
            queryset=Category.objects.visible().opened().ordered(),
            related_name='category_set',
            parent_field='parent_id',
            label_field='title',
            label=_("Category"),
            empty_label=_("Choose a category"))

        if self.instance.pk and not user.st.is_moderator:
            del self.fields['category']

        self.fields['assignee'] = forms.ModelChoiceField(
            queryset=User.objects.filter(st__is_assignee=True),
            label=_("Assignee"),
            required=False,
            blank=True,
            empty_label=_("Choose an assignee (optional)"))

    def get_category(self):
        return self.cleaned_data['category']

    def get_topic_hash(self):
        topic_hash = self.cleaned_data.get('topic_hash', None)

        if topic_hash:
            return topic_hash

        return utils.get_hash((
            smart_bytes(self.cleaned_data['title']),
            smart_bytes('category-{}'.format(self.cleaned_data['category'].pk))))

    def save(self, commit=True):
        if not self.instance.pk:
            self.instance.user = self.user

        self.instance.reindex_at = timezone.now()
        return super(TopicForm, self).save(commit)
