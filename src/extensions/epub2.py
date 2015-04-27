import os
import shutil
from sphinx.builders.epub import EpubBuilder


# We subclass EpubBuilder and re-define build_epub to call
# clean_html_file_for_ibooks. This function replaces all instances of
# the SPAN tag to SAMP. It's uglish but it works. A better way would
# be to change sphinx.writers.html to emmit the SAMP tag in the first
# place, but it seems even more difficult to do.


def clean_html_file_for_ibooks(filename):
    bakname = filename + ".bak"
    shutil.move(filename, bakname)
    destination = open(filename, 'w')
    original = open(bakname, 'r')

    for line in original:
        txt = line.replace("<span", "<samp").replace("</span>", "</samp>")
        destination.write(txt)

    destination.close()
    original.close()
    os.remove(bakname)


class AppEpubBuilder(EpubBuilder):
    name = "epub2"

    def build_epub(self, outdir, outname):
        self.info('cleaning html files...')
        for item in self.files:
            if item.endswith("html"):
                clean_html_file_for_ibooks(os.path.join(outdir, item))

        super(AppEpubBuilder, self).build_epub(outdir, outname)


def setup(app):
    app.add_builder(AppEpubBuilder)
