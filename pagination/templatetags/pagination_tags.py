try:
    set
except NameError:
    from sets import Set as set

from django import template
from django.http import Http404
from django.core.paginator import Paginator, InvalidPage
from django.conf import settings

register = template.Library()

DEFAULT_PAGINATION = getattr(settings, 'PAGINATION_DEFAULT_PAGINATION', 20)
DEFAULT_WINDOW = getattr(settings, 'PAGINATION_DEFAULT_WINDOW', 4)
DEFAULT_ORPHANS = getattr(settings, 'PAGINATION_DEFAULT_ORPHANS', 0)
INVALID_PAGE_RAISES_404 = getattr(settings, 'PAGINATION_INVALID_PAGE_RAISES_404',
    False)

def do_autopaginate(parser, token):
    """
    Splits the arguments to the autopaginate tag and formats them correctly.
    """
    split = token.split_contents()
    as_index = None
    context_var = None
    for i, bit in enumerate(split):
        if bit == 'as':
            as_index = i
            break
    if as_index is not None:
        try:
            context_var = split[as_index + 1]
        except IndexError:
            raise template.TemplateSyntaxError("Context variable assignment " +\
                "must take the form of {%% %r object.example_set.all ... as " +\
                "context_var_name %%}" % split[0])
        del split[as_index:as_index + 2]
    if len(split) == 2:
        return AutoPaginateNode(split[1])
    elif len(split) == 3:
        return AutoPaginateNode(split[1], paginate_by=split[2], 
            context_var=context_var)
    elif len(split) == 4:
        try:
            orphans = int(split[3])
        except ValueError:
            raise template.TemplateSyntaxError(u'Got %s, but expected integer.' % split[3])
        return AutoPaginateNode(split[1], paginate_by=split[2], orphans=orphans,
            context_var=context_var)
    else:
        raise template.TemplateSyntaxError('%r tag takes one required ' + \
            'argument and one optional argument' % split[0])

class AutoPaginateNode(template.Node):
    """
    Emits the required objects to allow for Digg-style pagination.
    
    First, it looks in the current context for the variable specified, and using
    that object, it emits a simple ``Paginator`` and the current page object 
    into the context names ``paginator`` and ``page_obj``, respectively.
    
    It will then replace the variable specified with only the objects for the
    current page.
    
    .. note::
        
        It is recommended to use *{% paginate %}* after using the autopaginate
        tag.  If you choose not to use *{% paginate %}*, make sure to display the
        list of available pages, or else the application may seem to be buggy.
    """
    def __init__(self, queryset_var, paginate_by=DEFAULT_PAGINATION,
        orphans=DEFAULT_ORPHANS, context_var=None):
        self.queryset_var = template.Variable(queryset_var)
        if isinstance(paginate_by, int):
            self.paginate_by = paginate_by
        else:
            self.paginate_by = template.Variable(paginate_by)
        self.orphans = orphans
        self.context_var = context_var

    def render(self, context):
        key = self.queryset_var.var
        value = self.queryset_var.resolve(context)
        if isinstance(self.paginate_by, int):
            paginate_by = self.paginate_by
        else:
            paginate_by = self.paginate_by.resolve(context)
        paginator = Paginator(value, paginate_by, self.orphans)
        try:
            page_obj = paginator.page(context['request'].page)
        except InvalidPage:
            if INVALID_PAGE_RAISES_404:
                raise Http404('Invalid page requested.  If DEBUG were set to ' +
                    'False, an HTTP 404 page would have been shown instead.')
            context[key] = []
            context['invalid_page'] = True
            return u''
        if self.context_var is not None:
            context[self.context_var] = page_obj.object_list
        else:
            context[key] = page_obj.object_list
        context['paginator'] = paginator
        context['page_obj'] = page_obj
        return u''

def paginate(context, window=DEFAULT_WINDOW):
    """
    Renders the ``pagination/pagination.html`` template, resulting in a
    Digg-like display of the available pages, given the current page.  If there
    are too many pages to be displayed before and after the current page, then
    elipses will be used to indicate the undisplayed gap between page numbers.
    
    Requires one argument, ``context``, which should be a dictionary-like data
    structure and must contain the following keys:
    
    ``paginator``
        A ``Paginator`` or ``QuerySetPaginator`` object.
    
    ``page_obj``
        This should be the result of calling the page method on the 
        aforementioned ``Paginator`` or ``QuerySetPaginator`` object, given
        the current page.
    
    This same ``context`` dictionary-like data structure may also include:
    
    ``getvars``
        A dictionary of all of the **GET** parameters in the current request.
        This is useful to maintain certain types of state, even when requesting
        a different page.
        """
    try:
        paginator = context['paginator']
        page_obj = context['page_obj']
        page_range = paginator.page_range
        # First and last are simply the first *n* pages and the last *n* pages,
        # where *n* is the current window size.
        first = set(page_range[:window])
        last = set(page_range[-window:])
        # Now we look around our current page, making sure that we don't wrap
        # around.
        current_start = page_obj.number-1-window
        if current_start < 0:
            current_start = 0
        current_end = page_obj.number-1+window
        if current_end < 0:
            current_end = 0
        current = set(page_range[current_start:current_end])
        pages = []
        # If there's no overlap between the first set of pages and the current
        # set of pages, then there's a possible need for elusion.
        if len(first.intersection(current)) == 0:
            first_list = list(first)
            first_list.sort()
            second_list = list(current)
            second_list.sort()
            pages.extend(first_list)
            diff = second_list[0] - first_list[-1]
            # If there is a gap of two, between the last page of the first
            # set and the first page of the current set, then we're missing a
            # page.
            if diff == 2:
                pages.append(second_list[0] - 1)
            # If the difference is just one, then there's nothing to be done,
            # as the pages need no elusion and are correct.
            elif diff == 1:
                pass
            # Otherwise, there's a bigger gap which needs to be signaled for
            # elusion, by pushing a None value to the page list.
            else:
                pages.append(None)
            pages.extend(second_list)
        else:
            unioned = list(first.union(current))
            unioned.sort()
            pages.extend(unioned)
        # If there's no overlap between the current set of pages and the last
        # set of pages, then there's a possible need for elusion.
        if len(current.intersection(last)) == 0:
            second_list = list(last)
            second_list.sort()
            diff = second_list[0] - pages[-1]
            # If there is a gap of two, between the last page of the current
            # set and the first page of the last set, then we're missing a 
            # page.
            if diff == 2:
                pages.append(second_list[0] - 1)
            # If the difference is just one, then there's nothing to be done,
            # as the pages need no elusion and are correct.
            elif diff == 1:
                pass
            # Otherwise, there's a bigger gap which needs to be signaled for
            # elusion, by pushing a None value to the page list.
            else:
                pages.append(None)
            pages.extend(second_list)
        else:
            differenced = list(last.difference(current))
            differenced.sort()
            pages.extend(differenced)
        to_return = {
            'pages': pages,
            'page_obj': page_obj,
            'paginator': paginator,
            'is_paginated': paginator.count > paginator.per_page,
        }
        if 'request' in context:
            getvars = context['request'].GET.copy()
            if 'page' in getvars:
                del getvars['page']
            if len(getvars.keys()) > 0:
                to_return['getvars'] = "&%s" % getvars.urlencode()
            else:
                to_return['getvars'] = ''
        return to_return
    except KeyError, AttributeError:
        return {}
register.inclusion_tag('pagination/pagination.html', takes_context=True)(paginate)
register.tag('autopaginate', do_autopaginate)
