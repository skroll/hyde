import pygments
from pygments.formatters import HtmlFormatter
from pygments.util import get_bool_opt

class HydeHtmlFormatter(HtmlFormatter):
    def __init__(self, **options):
        HtmlFormatter.__init__(self, **options)
        self.wrap_pre = get_bool_opt(options, 'wrap_pre', False)
        self.wrap_code = get_bool_opt(options, 'wrap_code', False)

    def wrap(self, source, outfile):
        return self._wrap_code(source)

    def _wrap_code(self, source):
        html_line = ''
        if self.wrap_pre:
            html_line += '<pre>'
        if self.wrap_code:
            html_line += '<code>'
        yield 0, html_line

        for i, t in source:
            if i == 1:
                # it's a line of formatted code
                t += '<br>'
            yield i, t

        html_line = ''
        if self.wrap_code:
            html_line += '</code>'
        if self.wrap_pre:
            html_line += '</pre>'
        yield 0, html_line
