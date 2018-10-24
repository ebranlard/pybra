from userpath import PATH


def require(library=None,version=None):
    import sys
    p=PATH()
    if library:
        try:
            path=eval('p.%s'%library)
            if path in sys.path:
                # Possibly display library asked, handle multiple library versions etc..
                pass
            else:
                sys.path.insert(0,path)
                print('require: %s (%s)'%(library,path))
        except Exception,e:
            raise e

    

