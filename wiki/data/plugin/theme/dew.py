# -*- coding: iso-8859-1 -*-
"""
    MoinMoin acm theme

    Based on the classic theme.

    @copyright: 2006 by RadomirDopieralski (moose@sheep.prv.pl)
    @license: GNU GPL, see COPYING for details.
"""

from MoinMoin import wikiutil, version
from MoinMoin import caching
from MoinMoin.theme import ThemeBase
from MoinMoin.theme import rightsidebar
from MoinMoin.Page import Page

class Theme(rightsidebar.Theme):
    """ here are the functions generating the html responsible for
        the look and feel of your wiki site
    """
    
    name = "dew"

    # fake _ function to get gettext recognize those texts:
    _ = lambda x: x

    # TODO: remove icons that are not used any more.
    icons = {
        # key         alt                        icon filename      w   h
        # ------------------------------------------------------------------
        # navibar
        'help':       ("%(page_help_contents)s", "moin-help.gif",   24, 24),
        'find':       ("%(page_find_page)s",     "moin-search.gif", 24, 24),
        'diff':       (_("Diffs"),               "moin-diff.gif",   24, 24),
        'info':       (_("Info"),                "moin-info.gif",   24, 24),
        'edit':       (_("Edit"),                "moin-edit.gif",   24, 24),
        'unsubscribe':(_("Unsubscribe"),         "moin-unsubscribe.gif",  24, 24),
        'subscribe':  (_("Subscribe"),           "moin-subscribe.gif", 24, 24),
        'raw':        (_("Raw"),                 "moin-raw.gif",    24, 24),
        'xml':        (_("XML"),                 "moin-xml.gif",    24, 24),
        'print':      (_("Print"),               "moin-print.gif",  24, 24),
        'view':       (_("View"),                "moin-show.gif",   24, 24),
        'home':       (_("Home"),                "moin-home.gif",   24, 24),
        'up':         (_("Up"),                  "moin-parent.gif", 23, 23),
        # FileAttach
        'attach':     ("%(attach_count)s",       "moin-attach.gif", 24, 24),
        # RecentChanges
        'rss':        (_("[RSS]"),               "moin-rss.png",    36, 14),
        'deleted':    (_("[DELETED]"),           "moin-delete.gif", 24, 24),
        'updated':    (_("[UPDATED]"),           "moin-show.gif",24, 24),
        'new':        (_("[NEW]"),               "moin-edit.gif",    24, 24),
        'diffrc':     (_("[DIFF]"),              "moin-diff.gif",   24, 24),
        # General
        'bottom':     (_("[BOTTOM]"),            "moin-bottom.gif", 14, 10),
        'top':        (_("[TOP]"),               "moin-top.gif",    14, 10),
        'www':        ("[WWW]",                  "moin-www.gif",    11, 11),
        'mailto':     ("[MAILTO]",               "moin-email.gif",  14, 10),
        'news':       ("[NEWS]",                 "moin-news.gif",   10, 11),
        'telnet':     ("[TELNET]",               "moin-telnet.gif", 10, 11),
        'ftp':        ("[FTP]",                  "moin-ftp.gif",    11, 11),
        'file':       ("[FILE]",                 "moin-ftp.gif",    11, 11),
        # search forms
        'searchbutton': ("[?]",                  "moin-search.gif", 12, 12),
        'interwiki':  ("[%(wikitag)s]",          "moin-inter.gif",  16, 16),
    }
    del _

    def footer(self, d, **keywords):
        """ Assemble wiki footer
        
        @param d: parameter dictionary
        @keyword ...:...
        @rtype: unicode
        @return: page footer html
        """
        page = d['page']
        dict = {
            'username_html':  self.username(d),
            'page_footer1': self.emit_custom_html(self.cfg.page_footer1),
            'page_footer2': self.emit_custom_html(self.cfg.page_footer2),
            'page_info': self.pageinfo(page),
            'end_page': self.endPage(),
            'credits': self.credits(d),
            'version': self.showversion(d, **keywords),
            'navibar_html': self.navibar(d),
            'search_form_html': self.searchform(d),
            'editbar': self.editbar(d),
        }
        if not self.in_editor:
            return u'''
%(page_info)s%(end_page)s</div><div class="menu">
    <h1>Menu</h1>
    %(navibar_html)s
    %(search_form_html)s
    %(editbar)s
</div><div class="footer"><div id="footer">
    %(page_footer1)s
    %(username_html)s
    %(page_footer2)s
    %(credits)s
    %(version)s
</div></div></div></div></div>
'''%dict
        else:
            return u'''
%(page_info)s
%(end_page)s
</div>
'''%dict

    def iconbar(self, d):
        """
        Assemble the iconbar
        
        @param d: parameter dictionary
        @rtype: string
        @return: iconbar html
        """
        iconbar = []
        if self.cfg.page_iconbar and self.request.user.show_toolbar and d['page_name']:
            iconbar.append('<ul id="iconbar">\n')
            icons = self.cfg.page_iconbar[:]
            for icon in icons:
                if icon == "up":
                    if d['page_parent_page']:
                        iconbar.append('<li>%s</li>\n' % self.make_iconlink(icon, d))
                elif icon == "subscribe" and self.cfg.mail_enabled:
                    iconbar.append('<li>%s</li>\n' % self.make_iconlink(
                        ["subscribe", "unsubscribe"][self.request.user.isSubscribedTo([d['page_name']])], d))
                else:
                    iconbar.append('<li>%s</li>\n' % self.make_iconlink(icon, d))
            iconbar.append('</ul>\n')
        return ''.join(iconbar)
    
    def header(self, d):
        """
        Assemble page header
        
        @param d: parameter dictionary
        @rtype: string
        @return: page header html
        """
        self.in_editor = False;
        
        dict = {
            'config_header1_html': self.emit_custom_html(self.cfg.page_header1),
            'config_header2_html': self.emit_custom_html(self.cfg.page_header2),
            'logo_html':  self.logo(),
            'title_html':  self.title(d),
            'msg_html': self.msg(d),
            'trail_html': self.trail(d),
            'startpage_html': self.startPage(),
            'interwiki_html':  self.interwiki(d),
            'iconbar_html': self.iconbar(d),
        }
        dict.update(d)

#<div id="locationline">%(interwiki_html)s%(title_html)s</div>
        html = """
%(config_header1_html)s
<div class="cont1"><div class="cont2"><div class="cont3">
<div id="header"><div class="header"> 
%(logo_html)s
</div><div class="bar">
<div id="traildiv">%(trail_html)s</div>
%(msg_html)s
</div></div>%(config_header2_html)s<div class="content">%(iconbar_html)s%(startpage_html)s
""" % dict
        return html

    def editorheader(self, d):
        """
        Assemble page header for editor
        
        @param d: parameter dictionary
        @rtype: string
        @return: page header html
        """
        self.in_editor = True;
        
        dict = {
            'config_header1_html': self.emit_custom_html(self.cfg.page_header1),
            'config_header2_html': self.emit_custom_html(self.cfg.page_header2),
            'title_html': self.title(d),
            'msg_html': self.msg(d),
            'startpage_html': self.startPage(),
        }
        dict.update(d)

        html = """
<div class="editor">
%(config_header1_html)s

%(title_html)s
%(msg_html)s

%(config_header2_html)s

%(startpage_html)s
""" % dict
        return html

    def editbar(self, d):
        if self.request.user.valid:
            return rightsidebar.Theme.editbar(self, d)
        else:
            return ''

    def recentchanges_entry(self, d):
        """
        Assemble a single recentchanges entry (table row)

        @param d: parameter dictionary
        @rtype: string
        @return: recentchanges entry html
        """
        _ = self.request.getText
        html = []
        html.append('<tr>\n')

        html.append('<td class="rcicon1">%(icon_html)s</td>\n' % d)

        html.append('<td class="rcpagelink">%(pagelink_html)s</td>\n' % d)

        html.append('<td class="rctime">')
        if d['time_html']:
                        html.append("%(time_html)s" % d)
        html.append('</td>\n')

        html.append('<td class="rcicon2">%(info_html)s</td>\n' % d)

        html.append('<td class="rceditor">')
        if d['editors']:
                        html.append('<br>'.join(d['editors']))
        html.append('</td>\n')

        html.append('</tr><tr class="rccomment">')
        html.append('<td class="rccomment" colspan="5">')
        if d['comments']:
            if d['changecount'] > 1:
                notfirst = 0
                for comment in d['comments']:
                    html.append('%s<tt>#%02d</tt>&nbsp;%s' % (
                        notfirst and '<br>' or '' , comment[0], comment[1]))
                    notfirst = 1
            else:
                comment = d['comments'][0]
                html.append('%s' % comment[1])
        html.append('</td>\n')

        html.append('</tr>\n')

        return ''.join(html)

