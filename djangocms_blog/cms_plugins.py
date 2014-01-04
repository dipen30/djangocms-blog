# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import AuthorEntriesPlugin, LatestPostsPlugin, Post


class BlogPlugin(CMSPluginBase):

    module = 'Blog'


class LatestEntriesPlugin(BlogPlugin):

    render_template = 'djangocms_blog/plugins/latest_entries.html'
    name = _('Latest Blog Entries')
    model = LatestPostsPlugin

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context


class AuthorPostsPlugin(BlogPlugin):
    module = _('Blog')
    name = _('Author Blog posts')
    model = AuthorEntriesPlugin
    render_template = 'djangocms_blog/plugins/authors.html'
    filter_horizontal = ['authors']

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context


class BlogTagsPlugin(BlogPlugin):
    module = _('Blog')
    name = _('Tags')
    model = CMSPlugin
    render_template = 'djangocms_blog/plugins/tags.html'

    def render(self, context, instance, placeholder):
        context['tags'] = Post.objects.tag_cloud(queryset=Post.objects.published())
        return context


class BlogArchivePlugin(BlogPlugin):
    module = _('Blog')
    name = _('Archive')
    model = CMSPlugin
    render_template = 'djangocms_blog/plugins/archive.html'

    def render(self, context, instance, placeholder):
        context['dates'] = Post.objects.get_months(queryset=Post.objects.published())
        return context

plugin_pool.register_plugin(LatestEntriesPlugin)
plugin_pool.register_plugin(AuthorPostsPlugin)
plugin_pool.register_plugin(BlogTagsPlugin)
plugin_pool.register_plugin(BlogArchivePlugin)
