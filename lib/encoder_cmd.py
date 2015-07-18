import getopt, sys, os
import fun_lib,common_lib,as265_cmd_init,x26x_cmd_init,seq_list,hm_cmd_init,jm_cmd_init
import global_vars

class Encoder_prop:
  id=''
  exe=''
  help_exe=''
  version_exe=''
  conf='r'
  platform='x64'
  get_param_cmd=""
  __executors={'as265':'cli_ashevc.exe',
               'x265':'x265.exe',
               'x264': 'x264.exe',
               'hm':'hm.exe',
               'jm':'lencod.exe',
              }
  __helps={'as265': '',
           'x265': '--log-level full --help',
           'x264' : '--fullhelp',
           'hm':'--help',
           'jm':'-h'
           }
  __versions={'as265':'',
              'x265':'--version',
              'x264':'--version',
              'hm':'--version',
              'jm':'-V',
              }
  __confs={'as265':{'d':'Debug','r':'Release','R':'Release_WithTrace'},
           'x265':{'d':'Debug','r':'Release','R':'RelWithDebInfo'},
           'x264':{'d':'Debug','r':'Release','R':'Release'},
           'hm':{'d':'Debug','r':'Release','R':'Release'},
           'jm':{'d':'','r':'','R':''},
           }
  __platforms={'as265':{'x86':'x64','x64':'x64'},
               'x265':{'x86':'vc10-x86','x64':'vc10-x86_64'},
               'x264':{'x86':'Win32','x64':'x64'},
               'hm':{'x86':'Win32','x64':'x64'},
               'jm':{'x86':'','x64':''},
               }
  __cmd_func_list={
    "as265": as265_cmd_init.get_enc_param_cmd_as265,
    "x265": x26x_cmd_init.get_enc_param_cmd_x265,
    "x264": x26x_cmd_init.get_enc_param_cmd_x264,
    "hm": hm_cmd_init.get_enc_param_cmd_hm,
    "jm": jm_cmd_init.get_enc_param_cmd_jm,
  }
  #__paths = dict()
  #__paths['as265'] =
  #__paths['x265'] =
  #__paths['x264'] =
  __common_path = 'd:/workspace/'
  __x265_path="x265_v1.5_20150211"
  if global_vars.x265_ver=="v1.6":
    __x265_path="x265_v1.6_20150403"

  #hevc_path='hevc_enc'
  hevc_path='HEVC_Encoder'
  #__paths={'as265':__common_path + 'arcsoft_codes/HEVC_Codec/'+hevc_path+'/bin/x64/',
  #         'x265':__common_path+'src.x265/trunk/'+__x265_path+'/build/vc10-x86_64/',
  #         'x264':__common_path + 'src.x264/trunk/x264-snapshot-20140915-2245/bin/x64/',
  #         'hm':__common_path + 'src.hm/trunk/hm-10.0/bin/vc10/x64/'}
  __paths={'as265':os.path.join(__common_path , 'arcvideo_codes/HEVC_Codec/',hevc_path,'bin/x64/'),
           'x265':os.path.join(__common_path,'src.x265/trunk/',__x265_path,'build/vc10-x86_64/'),
           'x264':os.path.join(__common_path , 'src.x264/trunk/x264-snapshot-20140915-2245/bin/x64/'),
           'hm':os.path.join(__common_path , 'src.hm/trunk/hm-10.0/bin/vc10/x64/'),
           'jm':os.path.join(__common_path , 'SRC.JM/trunk/jm18.5/bin/'),
           }

  #@staticmethod
  #def __format_path(path):
  #  path=path.strip()
  #  path = os.path.normpath(path)#path.replace("\\", "/")
  #  if path[-1]!="/":
  #    path+="/"
  #  return path
  def __set_encoder_prop(self):
    Encoder_prop.__paths[self.id]=common_lib.format_path(Encoder_prop.__paths[self.id])
    #exe_str = Encoder_prop.__paths[self.id] + Encoder_prop.__executors[self.id]
    exe_str=os.path.join(Encoder_prop.__paths[self.id],Encoder_prop.__confs[self.id][self.conf],Encoder_prop.__executors[self.id])
    #exe_str = exe_str.replace("\\", "/")
    #sys_str = common_lib.determin_sys()
    #if sys_str == "cygwin" and exe_str.find("cygdrive") < 0:
    #  exe_str = "/cygdrive/" + exe_str.replace(":", "")
    self.exe=common_lib.normalize_path(exe_str)
    self.help_exe= self.exe + " "+Encoder_prop.__helps[self.id]
    self.version_exe=self.exe+" "+Encoder_prop.__versions[self.id]
    self.get_param_cmd=Encoder_prop.__cmd_func_list[self.id]

  def __set_id(self,id):
    tmp=id[-1]
    if tmp in ('d','r','R'):
      self.conf=tmp
      self.id=id[:-1]
    else:
      self.conf='r'
      self.id=id


  def __init__(self, id="as265"):
    #self.id = id
    self.__set_id(id)
    self.__set_encoder_prop()


  def set_encoder_id(self,id):
    #self.id=id
    self.__set_id(id)
    self.__set_encoder_prop()

  def set_encoder_path(self,path):
    Encoder_prop.__paths[self.id]=path
    self.__set_encoder_prop()

  @staticmethod
  def SET_PATH(id,path):
    Encoder_prop.__paths[id]=path



def configure_seq_param(param_list, tmp_name,tmp_width=-1,tmp_height=-1,tags=""):
  seq_name=seq_list.guess_seqname(tmp_name)
  org_width, org_height, org_fps = fun_lib.get_reso_info(seq_name)
  #tmp_width=tmp_list['tmp_nSrcWidth']
  #tmp_height=tmp_list['tmp_nSrcHeight']
  if tmp_width<=0 or tmp_height<=0:
    param_list['nSrcWidth'] = int(org_width)
    param_list['nSrcHeight'] = int(org_height)
  else:
    param_list['nSrcWidth'] = int(tmp_width)
    param_list['nSrcHeight'] = int(tmp_height)
  param_list['fFrameRate'] = int(org_fps)

  if tags!="":
    tags="_"+tags
  param_list['input_filename'] = seq_name + ".yuv"
  param_list['output_filename'] = seq_name + tags + "_str.bin"
  param_list['trace_file_cabac'] = seq_name + tags + "_cabac.log"
  param_list['trace_file_general'] = seq_name + tags + "_general.log"
  param_list['dump_file_rec'] = seq_name + tags + "_rec.yuv"
  param_list['trace_file_prd_y'] = seq_name + tags + "_prdy.log"
  param_list['trace_file_prd_uv'] = seq_name + tags + "_prduv.log"
  param_list['trace_file_cabacrdo'] = seq_name + tags + "_cabacrdo.log"
  param_list['trace_file_arch1rdo'] = seq_name + tags + "_arch1rdo.log"

  return seq_name+tags+"_cons.log"

def set_rc_related_param_manual(param_list, bitrate, vbv_maxrate, vbv_buffer_size):
  param_list['nBitrate'] = bitrate
  param_list['nMaxBitrate'] = vbv_maxrate
  param_list['vbv_buffer_size'] = vbv_buffer_size
  #if bitrate == 0:
  #  param_list['eRcType'] = 0
  #elif vbv_maxrate == 0 or vbv_buffer_size == 0:
  #  param_list['eRcType'] = 8
  #elif vbv_maxrate <= bitrate:
  #  param_list['eRcType'] = 1
  #else:
  #  param_list['eRcType'] = 9

  return

def set_rc_related_param_auto(param_list, factor=2):
  rc_param = fun_lib.get_bitrate_for_rc(param_list['eRcType'], param_list['nSrcWidth'], param_list['nSrcHeight'], param_list['fFrameRate'], factor)
  #param_list['nBitrate'] = rc_param[0]
  #param_list['nMaxBitrate'] = rc_param[1]
  #param_list['vbv_buffer_size'] = rc_param[2]
  set_rc_related_param_manual(param_list,rc_param[0],rc_param[1],rc_param[2])
  return


def set_rc_related_param_semi_auto(param_list, bitrate):
  if bitrate<=0:
    #param_list['eRcType']=0
    set_rc_related_param_auto(param_list)
    return
  if bitrate<=1.0:
    bitrate*=param_list['nSrcWidth']*param_list['nSrcHeight']*param_list['fFrameRate']/1000
  bitrate=int(bitrate)
  vbv_maxrate=0
  if param_list['eRcType']==1:
    vbv_maxrate=bitrate
  elif param_list['eRcType']==3:
    vbv_maxrate=3*bitrate
  vbv_bufsize=vbv_maxrate*1
  set_rc_related_param_manual(param_list,bitrate,vbv_maxrate,vbv_bufsize)
  return


def usage():
  help_msg = '''Usage:./test.py [option] [value]...
  options:
   -e <string> encoder name:as265,x265,x264,hm,jm
   -i <string> input_path
   -o <string> output_path
   -I <integer> I frame interval
   -f <integer> frames to be encoded
   -F <integer> frame parallelism threads
   -W <integer> WPP threads
   -L <integer> Lookahead threads
   -l <integer> number of lookahead frames
   -h print this help
   -H print the help of encoder
   -q <integer> qp
   -r <integer> ratecontrol method
   -B <integer> bitrate
   -V <integer> vbv_max_bitrate
   -S <integer> vbv_buffer_size
   -b <integer> bframes
   -M <integer> bref/b-pyramid/hierarchical:0 disabled, 1 enabled
   -a <integer> aq-mode:0 disabled, 1 Variance AQ, Auto-Variance AQ
   -s <string> seqname
   -R <string> ref number
   -t <integer> use vbv-init-time
   -y dump-yuv
   -C <string> extra command lines
   -O <integer> Lowres:0 auto, 1 semi, 2 quater
   -p <integer> rc pass:0~3
   -T <string>  stats file
   -g <string> the 2pass log file
   -P <integer> qp step
   -A <integer> cu tree:0 disabled, 1 enabled
   -E <intxint> resolution: widthxheight
   -c <integer> scenecut value
   -G <integer> open-gop:0 disabled, 1 enabled
   -D <integer> bframe adaptive
   --version show the version info
   -k <integer> seek frame
   -j <integer> sao: 0 disabled, 1 enabled
   -J <integer> deblock: 0 disabled, 1 enabled
   '''
  print help_msg
  return


def get_tag(opt, arg):
  str = opt[1:] + arg
  return str


def parse_enc_cl(enc):
  if len(sys.argv) == 1:
    usage()
    sys.exit()

  try:
    opts, args = getopt.getopt(sys.argv[1:],
                               'i:o:I:f:F:W:L:l:hHq:r:B:V:S:b:M:a:s:R:e:t:yC:O:p:T:g:P:A:E:c:G:D:k:j:J:',['version',])
  except getopt.GetoptError as err:
    print str(err)
    sys.exit(2)
  except Exception, e:
    print e

  opt_list = {}#dict()
  tag_str = ""
  #seq_name = ""
  #tmp_nBitrate = -1
  #tmp_nMaxBitrate = -1
  #tmp_vbv_buffer_size = -1

  Help_flag=0
  Version_flag=0
  Encoder_flag=0

  for opt, arg in opts:
    if opt == "-i":
      opt_list["input_path"] = arg
    elif opt == "-o":
      opt_list["output_path"] = arg
    elif opt == "-I":
      opt_list["nIntraPicInterval"] = int(arg)
      tag_str += get_tag(opt, arg)
    elif opt == "-f":
      opt_list["frame_num_to_encode"] = int(arg)
      tag_str += get_tag(opt, arg)
    elif opt == "-F":
      opt_list["frame_threads"] = int(arg)
      tag_str += get_tag(opt, arg)
    elif opt == "-W":
      opt_list["wpp_threads"] = int(arg)
      tag_str += get_tag(opt, arg)
    elif opt == "-L":
      opt_list["lookahead_threads"] = int(arg)
      tag_str += get_tag(opt, arg)
    elif opt == "-l":
      opt_list["rc_i_lookahead"] = int(arg)
      tag_str += get_tag(opt, arg)
    elif opt == "-h":
      usage()
      sys.exit()
    elif opt == "-H":
      #print_encoder_help(encoder_id)
      Help_flag=1
    elif opt == "-q":
      opt_list["nQp"] = int(arg)
      tag_str += get_tag(opt, arg)
    elif opt == "-r":
      opt_list["eRcType"] = int(arg)
      tag_str += get_tag(opt, arg)
    elif opt == "-B":
      #tmp_nBitrate = int(arg)
      opt_list['tmp_nBitrate'] = int(arg)
      tag_str += get_tag(opt, arg)
    elif opt == "-V":
      #tmp_nMaxBitrate = int(arg)
      opt_list['tmp_nMaxBitrate'] = int(arg)
      tag_str += get_tag(opt, arg)
    elif opt == "-S":
      #tmp_vbv_buffer_size = int(arg)
      opt_list['tmp_vbv_buffer_size'] = int(arg)
      tag_str += get_tag(opt, arg)
    elif opt == "-b":
      opt_list["nBframe"] = int(arg)
      tag_str += get_tag(opt, arg)
    elif opt == "-M":
      opt_list["bExistRefB"] =int(arg)
      tag_str += get_tag(opt, arg)
    elif opt == "-a":
      opt_list["rc_i_aq_mode"] = int(arg)
      tag_str += get_tag(opt, arg)
    elif opt == "-s":
      #seq_name = arg
      opt_list['seq_name'] = arg
    elif opt == "-R":
      opt_list["nMaxRefNum"] = int(arg)
      tag_str += get_tag(opt, arg)
    elif opt == "-e":
      #opt_list["encoder_id"] = arg
      enc.set_encoder_id(arg.strip())
      Encoder_flag=1
    elif opt == "-t":
      opt_list["vbv_buffer_init_time"] = int(arg)
      tag_str += get_tag(opt, arg)
    elif opt == "-y":
      opt_list["trace_flag"] |= 2
    elif opt == "-C":
      opt_list["extra_cls"]=arg
      tag_str +=get_tag(opt,"")
    elif opt == "-O":
      opt_list["rc_i_lowres"] = int(arg)
      tag_str += get_tag(opt, arg)
    elif opt == "-p":
      opt_list["rc_i_pass"] = int(arg)
      tag_str += get_tag(opt, arg)
    elif opt == "-g":
      opt_list["rc_s_stats"] = arg
      tag_str += get_tag(opt, arg)
    elif opt == "-P":
      opt_list["rc_i_qp_step"] = int(arg)
      tag_str += get_tag(opt, arg)
    elif opt == "-A":
      opt_list["rc_b_cutree"] = int(arg)
      tag_str += get_tag(opt, arg)
    elif opt == "-E":
      tmp_width, tmp_height = arg.split('x')
      opt_list["tmp_nSrcWidth"] = int(tmp_width)
      opt_list["tmp_nSrcHeight"] = int(tmp_height)
      tag_str += get_tag(opt, arg)
    elif opt == "-c":
      opt_list["i_scenecut_threshold"] = int(arg)
      tag_str += get_tag(opt, arg)
    elif opt == "-G":
      opt_list["b_open_gop"] = int(arg)
      tag_str += get_tag(opt, arg)
    elif opt == "-D":
      opt_list["i_bframe_adaptive"] = int(arg)
      tag_str += get_tag(opt, arg)
    elif opt in ('--version',):
      Version_flag=1
    elif opt in ("-k",):
      opt_list["first_frame"] = int(arg)
      tag_str += get_tag(opt, arg)
    elif opt in ("-j",):
      opt_list["b_sao"] = int(arg)
      tag_str += get_tag(opt, arg)
    elif opt in ("-J",):
      opt_list["b_dbl"] = int(arg)
      tag_str += get_tag(opt, arg)
    else:
      assert False, "unknown option"

  if Help_flag==1:
    os.system(enc.help_exe)
    sys.exit()

  if Version_flag==1:
    os.system(enc.version_exe)
    sys.exit()

  if Encoder_flag==1:
    if tag_str=="":
      tag_str=enc.id
    else:
      tag_str=enc.id+"_"+tag_str

  #return (opt_list, tag_str, seq_name, tmp_nBitrate, tmp_nMaxBitrate, tmp_vbv_buffer_size)
  return (opt_list, tag_str)


def check_path(path):
    path=path.strip()#delete the blankspace before or after the path
    path=path.strip('\\')
    path=path.strip('/')
    #chech whether the path exists or creat it
    if not os.path.exists(path):
      os.makedirs(path)

def delete_files(path,ext_list):
  path=os.path.normpath(path)
  for root,dirs,files in os.walk(path):
    for fname in files:
      full_name=os.path.join(root,fname)
      ext=os.path.splitext(full_name)[1]
      if ext in ext_list:
        os.remove(full_name)

def remove_some_tmp_files(path):
  ext_list=(".bin",".rcstat",".pinfo",".log")
  delete_files(path,ext_list)

def check_files(param_list):
  #check the input file
  input_fullname=os.path.join(param_list['input_path'],param_list['input_filename'])
  if not os.path.exists(input_fullname):
    print "input file (%s) does not exist. Please check"%input_fullname
    sys.exit()

  #check the outputfiles: if exists, delete it
  output_fullname=os.path.join(param_list['output_path'],param_list['output_filename'])
  if os.path.exists(output_fullname):
    os.remove(output_fullname)
    print "Deleted output file: %s"%output_fullname

  output_fullname=os.path.join(param_list['output_path'],param_list['trace_file_cabac'])
  if os.path.exists(output_fullname):
    os.remove(output_fullname)
    print "Deleted output file: %s"%output_fullname

  output_fullname=os.path.join(param_list['output_path'],param_list['trace_file_general'])
  if os.path.exists(output_fullname):
    os.remove(output_fullname)
    print "Deleted output file: %s"%output_fullname

  output_fullname=os.path.join(param_list['output_path'],param_list['trace_file_prd_y'])
  if os.path.exists(output_fullname):
    os.remove(output_fullname)
    print "Deleted output file: %s"%output_fullname

  output_fullname=os.path.join(param_list['output_path'],param_list['trace_file_prd_uv'])
  if os.path.exists(output_fullname):
    os.remove(output_fullname)
    print "Deleted output file: %s"%output_fullname

  output_fullname=os.path.join(param_list['output_path'],param_list['trace_file_cabacrdo'])
  if os.path.exists(output_fullname):
    os.remove(output_fullname)
    print "Deleted output file: %s"%output_fullname

  output_fullname=os.path.join(param_list['output_path'],param_list['trace_file_arch1rdo'])
  if os.path.exists(output_fullname):
    os.remove(output_fullname)
    print "Deleted output file: %s"%output_fullname


def get_total_frame_num(filename,width,height):
  size=os.path.getsize(filename)
  filesize=width*height*3/2
  num_frames=size/filesize
  return num_frames

def check_params(param_list):
  param_list['output_path']=common_lib.format_path(param_list['output_path'])
  param_list['input_path']=common_lib.format_path(param_list['input_path'])

  check_path(param_list['output_path'])
  check_files(param_list)

  if param_list['frame_num_to_encode']<=0:
    param_list['frame_num_to_encode']=get_total_frame_num(os.path.join(param_list['input_path'],param_list['input_filename']),
                                                          param_list['nSrcWidth'],param_list['nSrcHeight'])
  return

def configure_rc_param(param_list,tmp_list):
  rc_type = param_list['eRcType']

  if rc_type != 0 and rc_type != 9:
    if tmp_list['tmp_nBitrate'] <= 0:
      set_rc_related_param_auto(param_list)
      return
    elif rc_type == 8 and tmp_list['tmp_nBitrate'] > 0:
      tmp_list['tmp_nMaxBitrate']=0
      tmp_list['tmp_vbv_buffer_size']=0
      #set_rc_related_param_manual(param_list, tmp_nBitrate, 0, 0)
    elif rc_type == 1 and tmp_list['tmp_nBitrate'] > 0:
      if tmp_list['tmp_nMaxBitrate'] <= 0:
        tmp_list['tmp_nMaxBitrate'] = tmp_list['tmp_nBitrate']
      if tmp_list['tmp_vbv_buffer_size'] <= 0:
        tmp_list['tmp_vbv_buffer_size'] = tmp_list['tmp_nMaxBitrate']
        #set_rc_related_param_manual(param_list, tmp_nBitrate, tmp_nMaxBitrate, tmp_vbv_buffer_size)
    elif rc_type == 3 and tmp_list['tmp_nBitrate'] > 0:
      if tmp_list['tmp_nMaxBitrate'] <= 0:
        tmp_list['tmp_nMaxBitrate'] = 3 * tmp_list['tmp_nBitrate']
      if tmp_list['tmp_vbv_buffer_size'] <= 0:
        tmp_list['tmp_vbv_buffer_size'] = tmp_list['tmp_nMaxBitrate']
        #set_rc_related_param_manual(param_list, tmp_nBitrate, tmp_nMaxBitrate, tmp_vbv_buffer_size)
    set_rc_related_param_manual(param_list, tmp_list['tmp_nBitrate'], tmp_list['tmp_nMaxBitrate'], tmp_list['tmp_vbv_buffer_size'])
    return

def get_default_tmp_list(param_list):
  tmp_list={}#dict()
  tmp_list['seq_name']=os.path.splitext(param_list['input_filename'])[0]#param_list['input_filename'].replace(".yuv","")
  tmp_list['tmp_nBitrate'] = -1
  tmp_list['tmp_nMaxBitrate'] = -1
  tmp_list['tmp_vbv_buffer_size'] = -1
  tmp_list['extra_cls']=""
  tmp_list['tmp_nSrcWidth']=-1
  tmp_list['tmp_nSrcHeight']=-1
  return tmp_list

def configure_enc_param(enc,param_list):
  tag_str=""
  tmp_list=get_default_tmp_list(param_list)
  param_len=len(param_list)
  tmp_list_len=len(tmp_list)

  if len(sys.argv)> 1:
    #opt_list, tag_str, seq_name, tmp_nBitrate, tmp_nMaxBitrate, tmp_vbv_buffer_size = parse_cl(enc)
    opt_list, tag_str = parse_enc_cl(enc)
    for (k, v) in opt_list.items():
      if param_list.has_key(k):
        param_list[k] = v
      else:
        #print "Bug may exist in this program"
        tmp_list[k]=v
    if param_len!=len(param_list):
      print "dict(param_list) has been changed somewhere. Please fix this bug."
      sys.exit()
    if tmp_list_len!=len(tmp_list):
      print "dict(tmp_list) has been changed somewhere. Please fix this bug."
      sys.exit()

  cons_log=configure_seq_param(param_list, tmp_list['seq_name'],tmp_list['tmp_nSrcWidth'],tmp_list['tmp_nSrcHeight'],tag_str)

  configure_rc_param(param_list,tmp_list)

  check_params(param_list)

  return (cons_log,tmp_list['extra_cls'])


def get_full_cdec_cmd(enc,param_list):
  #param_cmd=""
  #if enc.id=="as265":
  #  param_cmd=as265_cmd_init.get_param_cmd_as265(param_list)
  #elif enc.id=="x265":
  #  param_cmd=x26x_cmd_init.get_param_cmd_x265(param_list)
  #elif enc.id=="x264":
  #  param_cmd=x26x_cmd_init.get_param_cmd_x264(param_list)
  param_cmd=enc.get_param_cmd(param_list)
  exe=enc.exe
  full_cmd_line=exe+" "+param_cmd
  return full_cmd_line
