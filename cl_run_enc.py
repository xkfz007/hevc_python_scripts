#!/usr/bin/python
import os
import sys
import lib
import subprocess

encoder_id = "as265"
enc = lib.Encoder_prop(encoder_id)
# lib.Encoder_prop.SET_PATH("as265",r"D:\workspace\arcvideo_codes\HEVC_Codec\HEVC_Encoder3\bin\x64")
lib.Encoder_prop.SET_PATH("x265",
                          r"D:\workspace\arcvideo_codes\HEVC_Codec\HEVC_Encoder\tool_X265_stable_2015_02_14_b6be305a2f99_modified_for_performance_test\build\vc10-x86_64")

param_list = lib.get_default_enc_param_list()
# param_list['encder_exe']=lib.get_encoder_exe()
#param_list['output_path']="F:/encoder_test_output/as265_output/"
#param_list['input_path']="E:/sequences/"
#param_list['frame_num_to_encode']=100

#param_list['input_filename']="BlowingBubbles_416x240_50.yuv"
#seq_name="BlowingBubbles_416x240_50"
#param_list['eRcType']=1

cons = "tmp_cons.log"
#if len(sys.argv)> 1:
cons, extra_cls = lib.configure_enc_param(enc, param_list)

cmd_line = lib.get_full_cdec_cmd(enc, param_list)
cmd_line += " " + extra_cls

#reg_file = None
#if lib.determin_sys() == "cygwin":
#    cmd_line += (" 2>&1 |tee -a " + cons)
#    pf = open(cons, "w")
#    print >> pf, "%s" % cmd_line
#    pf.close()
#else:
#    reg_file = open(cons, 'w')
#
##os.system(cmd_line)
#print cmd_line
#subprocess.call(cmd_line, shell=True, stdout=reg_file, stderr=reg_file)
lib.run_cmd(cmd_line,cons,1)

