# -*- coding: utf-8 -*-
"""
Less css plugin
"""

from hyde.plugin import CLTransformer
from hyde.fs import File

import subprocess

class YuiCompressorPlugin(CLTransformer):
    """
    The plugin class for yuicompressor
    """

    def __init__(self, site):
        super(YuiCompressorPlugin, self).__init__(site)

    @property
    def executable_name(self):
        return "yuicompressor"

    @property
    def plugin_name(self):
        """
        The name of the plugin.
        """
        return "yuicompressor"

    def text_resource_complete(self, resource, text):
        """
        Save the file to a temporary place and run yuicompressor.
        Read the generated file and return the text as output.
        """

        try:
            mode = self.site.config.mode
        except AttributeError:
            mode = "production"

        if not resource.source_file.kind == 'css':
            return

        if mode.startswith('dev'):
            self.logger.debug("Skipping yuicompressor in development mode.")
            return

        yui = self.app

        source = File.make_temp(text)
        target = source

        args = [unicode(yui)]
        args.extend(["--type", "css"])
        args.extend(["-o", unicode(target), unicode(source)])

        try:
            self.call_app(args)
        except subprocess.CalledProcessError:
             raise self.template.exception_class(
                    "Cannot process %s. Error occurred when "
                    "processing [%s]" % (self.app.name, resource.source_file))

        return target.read_all()
