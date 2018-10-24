# --------------------------------------------------------------------------------
# --- USER DEFINED PATH FOR THE DIFFERENT LIBRARIES  
# --------------------------------------------------------------------------------
# 

class PATH:
    def __init__(self):
        import os
        # --------------------------------------------------------------------------------
        # --- LIBRARIES that are found in the OMNIVOR INC DIR 
        # --------------------------------------------------------------------------------
        omn_py_path=os.path.realpath(os.path.abspath(os.path.join(os.getenv('OMNIVOR_MKF_DIR', './'),'_PythonPath')))
        omn_tool_path=os.path.realpath(os.path.abspath(os.path.join(os.getenv('OMNIVOR_MKF_DIR', './'),'_tools')))
        
        self.MANN       = omn_tool_path
        # OLD, for compatibility
        self.DIV_FREE   = omn_tool_path
        self.OVERSAMPLE = omn_tool_path
        self.CLIP       = omn_tool_path
        self.ROT        = omn_tool_path
        self.PART       = omn_tool_path
        self.FIELD      = omn_tool_path
        #
        self.FILE_IO  = omn_py_path
        self.FORTRAN  = omn_py_path
        self.OFILE    = omn_py_path
        self.OMNIVOR  = omn_py_path
        
        self.FIELDS = omn_tool_path
