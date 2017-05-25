#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
from __future__ import unicode_literals
import os
import re
import sys
import math
import time
from CopybookGeneratorDlg import *
import svgwrite
import cairosvg
import pdfrw
from pypinyin import pinyin

   

ABOUT_INFO = '''\
字帖生成器 V1.0

URL: https://github.com/pengshulin/copybook_generator
Peng Shullin <trees_peng@163.com> 2017
'''

MODE = [
{
'name': 'A4 28*41',
'page_width': 21.0, 'page_height': 29.7, 'margin_x': 1.0, 'margin_y': 1.0,
'width': 0.67, 'height': 0.67, 'space_x': 0.0, 'space_y': 0.0,
'grid_type': '田字格',  'pinyin': False,  'font': '楷体',
'layout_type': '字帖',
},

{
'name': 'A4 24*35',
'page_width': 21.0, 'page_height': 29.7, 'margin_x': 1.0, 'margin_y': 1.0,
'width': 0.79, 'height': 0.79, 'space_x': 0.0, 'space_y': 0.0,
'grid_type': '田字格',  'pinyin': False,  'font': '楷体',
'layout_type': '字帖',
},

{
'name': 'A4 12*18',  # default
'page_width': 21.0, 'page_height': 29.7, 'margin_x': 1.5, 'margin_y': 1.5,
'width': 1.47, 'height': 1.47, 'space_x': 0.0, 'space_y': 0.0,
'grid_type': '米字格',  'pinyin': False,  'font': '楷体',
'layout_type': '字帖',
},

{
'name': 'A4 8*13',
'page_width': 21.0, 'page_height': 29.7, 'margin_x': 1.5, 'margin_y': 1.5,
'width': 2.0, 'height': 2.0, 'space_x': 0.0, 'space_y': 0.0,
'grid_type': '米字格',  'pinyin': False,  'font': '楷体',
'layout_type': '字帖',
},

{
'name': 'A4 6*9',
'page_width': 21.0, 'page_height': 29.7, 'margin_x': 1.5, 'margin_y': 1.5,
'width': 2.9, 'height': 2.9, 'space_x': 0.0, 'space_y': 0.0,
'grid_type': '米字格',  'pinyin': False,  'font': '楷体',
'layout_type': '字帖',
},

{
'name': 'A4 4*6',
'page_width': 21.0, 'page_height': 29.7, 'margin_x': 1.5, 'margin_y': 1.5,
'width': 4.4, 'height': 4.4, 'space_x': 0.0, 'space_y': 0.0,
'grid_type': '米字格',  'pinyin': False,  'font': '楷体',
'layout_type': '字帖',
},

{
'name': '5.5寸手机 6*10',
'page_width': 6.7, 'page_height': 12.1, 'margin_x': 0.3, 'margin_y': 0.3,
'width': 1.0, 'height': 1.0, 'space_x': 0.0, 'space_y': 0.0,
'grid_type': '米字格',  'pinyin': False,  'font': '楷体',
'layout_type': '字帖',
},

{
'name': '5.5寸手机 4*7',
'page_width': 6.7, 'page_height': 12.1, 'margin_x': 0.3, 'margin_y': 0.1,
'width': 1.5, 'height': 1.5, 'space_x': 0.0, 'space_y': 0.0,
'grid_type': '米字格',  'pinyin': False,  'font': '楷体',
'layout_type': '字帖',
},

{
'name': '6寸Kindle 8*10',
'page_width': 9, 'page_height': 12, 'margin_x': 0.1, 'margin_y': 0.1,
'width': 1.1, 'height': 1.1, 'space_x': 0.0, 'space_y': 0.0,
'grid_type': '米字格',  'pinyin': False,  'font': '楷体',
'layout_type': '字帖',
},

{
'name': '6寸Kindle 6*8',
'page_width': 9, 'page_height': 12, 'margin_x': 0.2, 'margin_y': 0.1,
'width': 1.4, 'height': 1.4, 'space_x': 0.0, 'space_y': 0.0,
'grid_type': '米字格',  'pinyin': False,  'font': '楷体',
'layout_type': '字帖',
},


]

                        
COLOR_REPEAT = []
for i in range(10):
    v = int(255*(1-1.0/float(i+1.0)))
    COLOR_REPEAT.append( '#%02X%02X%02X'% (v,v,v) )
#print COLOR_REPEAT


def conv(cfg):
    source = cfg['input']
    dirname = os.path.dirname(source)
    basename = os.path.basename(source)
    prefixname = os.path.splitext(basename)[0]
    outputdir = os.path.join(dirname, prefixname)
    pages_limit = cfg['pages_limit']

    unit = svgwrite.cm
    paper_w = cfg['page_width']
    paper_h = cfg['page_height']
    margin_x = cfg['margin_x']
    margin_y = cfg['margin_y']
    margin_left = margin_x
    margin_top = margin_y
    margin_right = paper_w - margin_x
    margin_bottom = paper_h - margin_y
    width = cfg['width']
    height = cfg['height']
    space_x = cfg['space_x']
    space_y = cfg['space_y']
    use_pinyin = cfg['pinyin']
    grid_type = cfg['grid_type']
    font = cfg['font']
    font_scale = cfg['font_scale']
    font_base = cfg['font_base']

    def read_source(fname, cfg):
        contents = []
        for c in open(fname, 'r').read().decode(encoding='utf8', errors='strict'):
            if c == u'_':
                c = u'　'
            else:
                c = c.strip()
            if c:
                contents.append(c)
            elif cfg['layout_type'] == '抄写词语':
                if contents and contents[-1] != 'EOL':
                    contents.append("EOL")
        #print contents
        return contents
 
    def draw_page( fname ):
        dwg = svgwrite.Drawing(fname, (paper_w*unit, paper_h*unit), debug=True)
        lines = dwg.add(dwg.g(stroke='grey'))

        height_pinyin = height * 0.3

        def draw_cell( x, y, w, h, grid_type='mi', color='black' ):
            # TODO: set line color
            x0, x1, x2, y0, y1, y2 = x, x+w/2, x+w, y, y+h/2, y+h
            l1=lines.add(dwg.line(start=(x0*unit, y0*unit), end=(x2*unit, y0*unit)))
            l2=lines.add(dwg.line(start=(x2*unit, y0*unit), end=(x2*unit, y2*unit)))
            l3=lines.add(dwg.line(start=(x0*unit, y2*unit), end=(x2*unit, y2*unit)))
            l4=lines.add(dwg.line(start=(x0*unit, y0*unit), end=(x0*unit, y2*unit)))

            if grid_type in ['米字格', '田字格']:
                l5=lines.add(dwg.line(start=(x0*unit, y1*unit), end=(x2*unit, y1*unit)))
                l6=lines.add(dwg.line(start=(x1*unit, y0*unit), end=(x1*unit, y2*unit)))
                l5.dasharray([2,2])
                l6.dasharray([2,2])
            if grid_type == '米字格':
                l7=lines.add(dwg.line(start=(x0*unit, y0*unit), end=(x2*unit, y2*unit)))
                l8=lines.add(dwg.line(start=(x0*unit, y2*unit), end=(x2*unit, y0*unit)))
                l7.dasharray([2,2])
                l8.dasharray([2,2])

        def draw_cell_pinyin( x, y, w, h, color='black' ):
            # TODO: set line color
            x0, x1, y0, y1, y2, y3 = x, x+w, y, y+h/3, y+h*2/3, y+h
            l1=lines.add(dwg.line(start=(x0*unit, y0*unit), end=(x1*unit, y0*unit)))
            l2=lines.add(dwg.line(start=(x1*unit, y0*unit), end=(x1*unit, y3*unit)))
            l3=lines.add(dwg.line(start=(x0*unit, y3*unit), end=(x1*unit, y3*unit)))
            l4=lines.add(dwg.line(start=(x0*unit, y0*unit), end=(x0*unit, y3*unit)))
            l5=lines.add(dwg.line(start=(x0*unit, y1*unit), end=(x1*unit, y1*unit)))
            l6=lines.add(dwg.line(start=(x0*unit, y2*unit), end=(x1*unit, y2*unit)))
            l5.dasharray([2,2])
            l6.dasharray([2,2])
 
        def get_new_char():
            try:
                return contents.pop(0)
            except:
                return None
 
        def draw_text( x, y, w, h, c, color='black' ):
            dwg.add( dwg.text(c, insert=((x+w/2)*unit,(y+h*((1+font_scale)/2-font_base))*unit), 
                     text_anchor=u'middle', font_family=font,
                     font_size=(h*font_scale)*unit, fill=color ) ) 
        
        def draw_text_pinyin( x, y, w, h, c, color='black' ):
            conv = pinyin(c)[0][0] 
            dwg.add( dwg.text(conv, insert=((x+w/2)*unit,(y+h*2/3)*unit),
                         text_anchor=u'middle', 
                    font_family=u'FreeSans', font_size=h*2/3*unit, fill=color ) ) 
        
        cursor_y = margin_top
        while cursor_y + height < margin_bottom:
            cursor_x = margin_left
            repeat_counter = 1 
            if cfg['layout_type'] == '抄写单字':
                c = get_new_char()
            elif cfg['layout_type'] == '抄写词语':
                cs = []
                while True:
                    nc = get_new_char()
                    if nc is None or nc == 'EOL':
                        break
                    else:
                        cs.append( nc )
                #print cs
                in_word_counter = 1
            while cursor_x + width < margin_right:
                if cfg['layout_type'] == '抄写单字':
                    if repeat_counter <= 3:
                        color = COLOR_REPEAT[repeat_counter-1]
                    else:
                        c = None
                    repeat_counter += 1
                elif cfg['layout_type'] == '抄写词语':
                    if repeat_counter <= 2:
                        try:
                            c = cs[in_word_counter-1]
                        except IndexError:
                            c = u'　'
                        color = COLOR_REPEAT[repeat_counter-1]
                    else:
                        c = None
                    if in_word_counter >= len(cs):
                        repeat_counter += 1
                        in_word_counter = 1
                    else:
                        in_word_counter += 1
                else:
                    c = get_new_char()
                    color = 'black'
                #print c
                lcolor = 'green'  # not used now
                if use_pinyin:
                    draw_cell_pinyin( cursor_x, cursor_y, width, height_pinyin, lcolor )
                    draw_cell( cursor_x, cursor_y+height_pinyin, width, height, grid_type, lcolor )
                    if c is not None:
                        draw_text( cursor_x, cursor_y+height_pinyin, width, height, c, color )
                        draw_text_pinyin( cursor_x, cursor_y, width, height_pinyin, c, color )
                        #print c,
                else:
                    draw_cell( cursor_x, cursor_y, width, height, grid_type, lcolor )
                    if c is not None:
                        draw_text( cursor_x, cursor_y, width, height, c, color )
                cursor_x += width + space_x
            if use_pinyin:
                cursor_y += height + height_pinyin + space_y
            else:
                cursor_y += height + space_y
        dwg.save()
        #print ''

    contents = read_source(source, cfg)
    page_index = 1
    if not os.path.isdir(outputdir):
        os.mkdir(outputdir)
    svgs, pdfs = [], []
    while contents:
        output_svg = os.path.join(outputdir, '%d.svg'% page_index )
        output_pdf = os.path.join(outputdir, '%d.pdf'% page_index )
        draw_page( output_svg )
        cairosvg.svg2pdf(url=output_svg, write_to=output_pdf)
        svgs.append( output_svg )
        pdfs.append( output_pdf )
        page_index += 1
        if pages_limit and (page_index > pages_limit):
            break
    # join pages 
    output_joined_pdf = os.path.join(outputdir, prefixname+'.pdf')
    writer = pdfrw.PdfWriter()
    for f in pdfs:
        writer.addpages(pdfrw.PdfReader(f).pages)
    writer.write( output_joined_pdf )
    # remove 
    if not cfg['keep_tempfiles']:
        #cmd = u'rm %s'% (' '.join(svgs + pdfs))
        #print cmd
        #os.system( cmd.encode(encoding='utf8') )
        for f in svgs + pdfs:
            os.remove(f)



class MainFrame(MyFrame):

    def __init__(self, *args, **kwds):
        MyFrame.__init__( self, *args, **kwds )
        self.Bind(wx.EVT_CLOSE, self.OnClose, self)
        self.combo_box_mode.AppendItems( [i['name'] for i in MODE] )
        self.combo_box_font.AppendItems( ['楷体', '隶书'] )
        self.combo_box_grid_type.AppendItems( ['米字格', '田字格', '口字格'] )
        self.combo_box_layout_type.AppendItems( ['字帖', '抄写单字', '抄写词语'] )
        self.combo_box_mode.SetValue('A4 12*18')
        self.doSelectMode()

    def OnClose(self, event):
        self.Destroy()
        event.Skip()
    
    def info( self, info, info_type=wx.ICON_WARNING ):
        if info:
            self.bar_info.ShowMessage(info, info_type)
        else:
            self.bar_info.Dismiss()
 
    def OnAbout(self, event):
        self.info( '' )
        dlg = wx.MessageDialog(self, ABOUT_INFO, '关于', wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
 
    def OnSelectInput(self, event):
        self.info( '' )
        dlg = wx.FileDialog( self, message="选择文件", defaultDir=os.getcwd(), 
                defaultFile='', wildcard="文本文件 (*.txt)|*.txt", style=wx.OPEN )
        if dlg.ShowModal() == wx.ID_OK:
            fname = dlg.GetPath().strip()
            self.text_ctrl_input.SetValue( fname )
            self.resetOutputName()
        dlg.Destroy()

    def OnInputText(self, event):
        self.resetOutputName()

    def resetOutputName(self):
        fname = self.text_ctrl_input.GetValue()
        if fname:
            dirname = os.path.dirname(fname)
            basename = os.path.basename(fname)
            prefixname = os.path.splitext(basename)[0]
            outputdir = os.path.join(dirname, prefixname)
            output_joined_pdf = os.path.join(outputdir, prefixname+'.pdf')
            self.text_ctrl_output.SetValue( output_joined_pdf )
        else:
            self.text_ctrl_output.SetValue( '' )
      
 
    def OnSelectPreMode(self, event):
        self.doSelectMode()

    def doSelectMode(self):
        sel = self.combo_box_mode.GetValue()
        for m in MODE:
            if m['name'] != sel:
                continue
            self.text_ctrl_page_width.SetValue( str(m['page_width']) )
            self.text_ctrl_page_height.SetValue( str(m['page_height']) )
            self.text_ctrl_margin_x.SetValue( str(m['margin_x']) )
            self.text_ctrl_margin_y.SetValue( str(m['margin_y']) )
            self.text_ctrl_width.SetValue( str(m['width']) )
            self.text_ctrl_height.SetValue( str(m['height']) )
            self.text_ctrl_space_x.SetValue( str(m['space_x']) )
            self.text_ctrl_space_y.SetValue( str(m['space_y']) )
            self.combo_box_font.SetValue( m['font'] )
            self.combo_box_grid_type.SetValue( m['grid_type'] )
            self.checkbox_pinyin.SetValue( m['pinyin'] )
            self.combo_box_layout_type.SetValue( m['layout_type'] )

    def OnGenerate(self, event):
        self.info( '' )
        try:
            cfg = {}
            cfg['page_width'] = float(self.text_ctrl_page_width.GetValue())
            cfg['page_height'] = float(self.text_ctrl_page_height.GetValue())
            cfg['margin_x'] = float(self.text_ctrl_margin_x.GetValue())
            cfg['margin_y'] = float(self.text_ctrl_margin_y.GetValue())
            cfg['width'] = float(self.text_ctrl_width.GetValue())
            cfg['height'] = float(self.text_ctrl_height.GetValue())
            cfg['space_x'] = float(self.text_ctrl_space_x.GetValue())
            cfg['space_y'] = float(self.text_ctrl_space_y.GetValue())
            cfg['font'] = self.combo_box_font.GetValue()
            cfg['grid_type'] = self.combo_box_grid_type.GetValue()
            cfg['pinyin'] = self.checkbox_pinyin.GetValue()
            cfg['input'] = self.text_ctrl_input.GetValue()
            cfg['output'] = self.text_ctrl_input.GetValue()
            cfg['keep_tempfiles'] = self.checkbox_keep_tempfiles.GetValue()
            cfg['pages_limit'] = int(self.text_ctrl_pages_limit.GetValue())
            cfg['layout_type'] = self.combo_box_layout_type.GetValue()
            cfg['font_scale'] = float(self.text_ctrl_font_scale.GetValue())
            cfg['font_base'] = float(self.text_ctrl_font_base.GetValue())
            if cfg['output']:
                conv( cfg )
            else:
                self.info( '请选择输入文件' )
        except Exception as e:
            self.info( u'错误 %s'% unicode(e), wx.ICON_ERROR )
            



if __name__ == "__main__":
    gettext.install("app")
    app = wx.App(0)
    app.SetAppName( 'CopybookGeneratorApp' )
    dialog_1 = MainFrame(None, wx.ID_ANY, "")
    app.SetTopWindow(dialog_1)
    dialog_1.Show()
    app.MainLoop()
