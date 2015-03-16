import sys, getopt
#import cgi

shell = 'shell.html'

def main(argv):
  configfile = ''
  showshelldir = ''
  outputdir = ''

  try:
    opts, args = getopt.getopt(argv,"hc:i:o:",["config=","showshell-dir=","output-dir="])
  except getopt.GetoptError:
    print 'usage: test.py -c <config file> -i <showshell directory> -o <output directory>'
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print 'usage: test.py -c <config file> -i <showshell directory> -o <output directory>'
      sys.exit()
    elif opt in ("-c"):
      configfile = arg
    elif opt in ("-i"):
      showshelldir = arg
    elif opt in ("-o"):
      outputdir = arg

  if(configfile == ''):
    print 'no -c <config file> given'
    sys.exit(2)
  if(showshelldir == ''):
    print 'no -i <showshell directory> given'
    sys.exit(2)
  if(outputdir == ''):
    print 'no -o <output directory> given'
    sys.exit(2)

  template = open(showshelldir + "/" + shell, 'r').read()

  config = open(configfile, 'r')
  content = config.readlines()

  title = ''
  linkstarted = False
  tabstarted = False
  runstarted = False
  tabtitle = ''
  collector = []
  runlist = []
  dependencylist = []
  tablist = []

  for line in content:
    line = line.strip()
    if line.startswith('{title:'):
      title = line.strip('{title:').strip().strip('}')
      continue

    if line == "{link}":
      linkstarted = True
      continue

    if line == "{run}":
      runstarted = True
      continue

    if line.startswith('{tab:'):
      tabtitle = line.strip('{tab:').strip().strip('}')
      tabstarted = True
      continue

    if line == "{end}":
      if (not linkstarted) and (not tabstarted) and (not runstarted):
        print "malformed config file. {end} found without starting {link}, {run} or {tab:NAME}"
        sys.exit(2)
      elif linkstarted:
        if len(dependencylist) > 0:
            print "cannot have more than one {link} section"
            sys.exit(2)
        dependencylist = list(collector)
      elif tabstarted:
        tablist.append((tabtitle, list(collector)))
      elif runstarted:
        if len(runlist) > 0:
            print "cannot have more than one {run} section"
            sys.exit(2)
        runlist = list(collector)

      collector = []
      linkstarted = False
      tabstarted = False
      runstarted = False
      continue

    if line != "":
      #collector.append(cgi.escape(line))
      collector.append(line)
      continue

  template = template.replace("{{TITLE}}",title)
  template = template.replace("{{RUN}}", ''.join(runlist))
  template = template.replace("{{LINK}}", ''.join(dependencylist))

  tabstring = ''
  tabcontentstring = ''
  extra = ' active'
  extraclass = ' class="active"'
  tabindex = 1
  for tab in tablist:
    tabtitle = tab[0]
    tabcontent = tab[1]
    tabstring += '<li' + extraclass + '><a href="#tab' + str(tabindex) + '">' + tabtitle + '</a></li>'
    tabcontentstring += '<div id="tab' + str(tabindex) + '" class="tab' + extra + '">' + ''.join(tabcontent) + '</div>'
    tabindex += 1
    extra = ''
    extraclass = ''

  template = template.replace("{{TABS}}", tabstring)
  template = template.replace("{{TABCONTENT}}", tabcontentstring)

  outputfile = open(outputdir + '/' + shell, 'w')
  outputfile.write(template)
  outputfile.close()

if __name__ == "__main__":
  main(sys.argv[1:])
