from numpy import mod
import pylab
from re import sub
import matplotlib as mpl
from .colors import rgb2hex, fColrs
from cycler import cycler

# Should be placed in some kind of InitClear
# mpl.rcParams['lines.linewidth'] = 1.55
# mpl.rcParams['font.size'] = 15
# # mpl.rcParams['axes.color_cycle']=[rgb2hex((c*255).astype(int)) for c in fColrs()]
# mpl.rcParams['axes.prop_cycle']=cycler(color=[rgb2hex((c*255).astype(int)) for c in fColrs()])

# mpl.rcParams['font.family'] = 'helvetica'
# line.set_dashes([8, 4, 2, 4, 2, 4]) 
#lg = a.legend()
# fr = lg.get_frame()
# fr.set_lw(0.2)
#
# --------------------------------------------------------------------------------
# --- Export parameters 
# --------------------------------------------------------------------------------
class FigureExportParams:
    def __init__(self):
        self.path=['./']
        self.width=None
        self.height=None
        self.title=None
        self.font=15
        self.btitle=False
        self.blatex=False
        self.bconstrained=False

_global_params = FigureExportParams()  


def setFigureFont(font):
    font=int(font)
    _global_params.font=font
    mpl.rcParams.update({'font.size': font})
    mpl.rcParams['font.size'] = font

def setFigureWidth(width):
    _global_params.width=width

def setFigureHeigth(height):
    _global_params.height=height

def setFigurePath(path):
    if type(path)==list:
        _global_params.path=path
    else:
        _global_params.path=[path]

def setFigureTitle(btitle):
    _global_params.btitle=btitle


# --------------------------------------------------------------------------------
# --- Some Tools
# --------------------------------------------------------------------------------
def title2filename(title):
    title=''.join([s.capitalize() for s in title.split()])
    return sub(r'[%|:;.\[ \]\\=^*_/]','',title)

# --------------------------------------------------------------------------------
# --- Exporter 
# --------------------------------------------------------------------------------

class FigureExporter:

    @staticmethod
    def print1figure(figName,titleLatexSafe,script_name,script_run_dir,script_run_date):
            print('in \\autoref{fig:%s}'%figName);
            print('% ---------------------------------- FIGURE --------------------------------------')
            print('%% From script: %s, folder: %s, %s'%(script_name,script_run_dir,script_run_date));
            print('\\noindent\\begin{figure}[!htb]\\centering%');
            print('  \\includegraphics[width=0.49\\textwidth]{%s}'%figName);
            print('  \\caption{%s}\\label{fig:%s}%%'%(titleLatexSafe,figName));
            print('\\end{figure}');
            print('% --------------------------------------------------------------------------------')
            print(' ')

    @staticmethod
    def print2figures(figName,figNameLast,titleLatexSafe,script_name,script_run_dir,script_run_date):
            print('in \\autoref{fig:%sMain}'%figNameLast);
            print('% ---------------------------------- FIGURES -------------------------------------')
            print('%% From script: %s, folder: %s, %s'%(script_name,script_run_dir,script_run_date));
            print('%% subfig a:  in \\autoref{fig:%s}'%figNameLast);
            print('%% subfig b:  in \\autoref{fig:%s}'%figName);
            print('\\noindent\\begin{figure}[!htb]\\centering%%');
            print('  \\begin{subfigure}[b]{0.49\\textwidth}\\centering \\includegraphics[width=\\textwidth]{%s}\\caption{}\\label{fig:%s}\\end{subfigure}%%'%(figNameLast,figNameLast));
            print('  \\begin{subfigure}[b]{0.49\\textwidth}\\centering \\includegraphics[width=\\textwidth]{%s}\\caption{}\\label{fig:%s}\\end{subfigure}%%'%(figName,figName));
            print('  \\caption{%s}\\label{fig:%sMain}%%'%(titleLatexSafe,figNameLast));
            print('\\end{figure}');
            print('% --------------------------------------------------------------------------------')
            print(' ')


    @staticmethod
    def export(fig,figformat,i=1,n=1,width=None,height=None,figNameLast='',script_name='',script_run_dir='',script_run_date=''):
        if i is None:
            i=1
        # params (for now, using global params)
        params=_global_params

        ax=fig.gca()
        fig_title=fig._suptitle
        ax_title=ax.get_title()
        # storing the title, figure name
        if fig_title is not None  and len(fig_title.get_text())>0:
            bAxisTitle=False
            title=fig_title.get_text()
        else:
            bAxisTitle=True
            title=ax_title
        titleLatexSafe = sub(r"[_%^]", "", title)
        # figure name from title or figure number
        if title=='' or (title is None):
            figName='%d'%i
        else:
            figName=title2filename(title);



        # remove figure title if needed
        if not params.btitle:
            if bAxisTitle:
                ax.set_title('')
            else:
                fig.suptitle('')
        
        if params.blatex :
            pass
#             for iax =1:length(axList)
#                 ax=axList(iax);
#                 format_ticks(ax,0.02,0.009,'FontSize',11); % font size useless, hgexport takes care of it

        if params.bconstrained:
            pass
        # Actually just using the loose figure is enough to keep what the user has inputted it seems
            #xlims=get(gca,'XLim');
            #ylims=get(gca,'YLim');
            #pause(1)
            #set(gca,'XLim',xlims);
            #set(gca,'YLim',ylims);

        # --------------------------------------------------------------------------------
        # --- Exporting in figure pathc
        # --------------------------------------------------------------------------------
        print('Export path: ',params.path)
        for ifp in range(len(params.path)):
            filename='%s%s.%s'%(params.path[ifp],figName,figformat);
            fig.savefig(filename)
            print('Figure file: ',filename)
            # restoring the title
            if bAxisTitle:
                ax.set_title(title)
            else:
                fig.suptitle(title)


        # --------------------------------------------------------------------------------
        # --- Generating latex code 
        # --------------------------------------------------------------------------------
        if mod(n,2)==0:
            if mod(i,2)==0:
                FigureExporter.print2figures(figName,figNameLast,titleLatexSafe,script_name,script_run_dir,script_run_date)
        else:
            if mod(i,2)==0:
                FigureExporter.print2figures(figName,figNameLast,titleLatexSafe,script_name,script_run_dir,script_run_date)
            else:
                if i==n:
                    FigureExporter.print1figure(figName,titleLatexSafe,script_name,script_run_dir,script_run_date)

        figNameLast=figName;
        return figNameLast


__exporter = FigureExporter()  


# --------------------------------------------------------------------------------
# --- Export call wrapper 
# --------------------------------------------------------------------------------
def export(figformat,fig=None,i=None,width=None,height=None):
    import inspect
    import os
    import os.path
    import datetime
    frame=inspect.stack()[2]
    script_name=os.path.basename(frame[0].f_code.co_filename)
    script_run_dir=os.getcwd()
    script_run_date=datetime.datetime.now().strftime('%Y/%m/%d')

    if fig is None:
        # We'll loop over all figures
        figures=[manager.canvas.figure for manager in pylab.matplotlib._pylab_helpers.Gcf.get_all_fig_managers()]
        figNameLast=''
        for i, figure in enumerate(figures):
            figNameLast=__exporter.export(fig=figure,figformat=figformat,i=(i+1),n=len(figures),width=width,height=height,figNameLast=figNameLast,script_name=script_name,script_run_dir=script_run_dir,script_run_date=script_run_date)

    else:
        __exporter.export(fig=fig,figformat=figformat,i=i,width=width,height=height,script_name=script_name,script_run_dir=script_run_dir,script_run_date=script_run_date)
        pass
    
    for ifp in range(len(_global_params.path)):
        print('Figure saved in: %s'%_global_params.path[ifp]);
    print(' ');

    pass

def export2pdf(fig=None,i=None,width=None,height=None):
    export('pdf',fig=fig,i=i,width=width,height=height)
def export2png(fig=None,i=None,width=None,height=None):
    export('png',fig=fig,i=i,width=width,height=height)
def export2eps(fig=None,i=None,width=None,height=None):
    export('png',fig=fig,i=i,width=width,height=height)


# --------------------------------------------------------------------------------
# --- Example/test 
# --------------------------------------------------------------------------------
def test_export():

    #from ebra.export import *
    from numpy import linspace,sin,pi
    from matplotlib import pyplot as plt
    setFigurePath('./')

    x=linspace(0,2*pi,100);
    plt.figure()
    plt.title('fig_python')
    plt.grid()
    plt.plot(x,sin(x),'-')
    plt.xlabel('x coordinate [m]')
    plt.ylabel('Velocity  U_i [m/s]')
    plt.xlim([0,2*pi])

    export2pdf()

if __name__ == "__main__":
    test_export()
