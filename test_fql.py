import foliadocserve
import sys

docstore = foliadocserve.DocStore(sys.argv[1], 900)

foliadocserve.parsequery("IN proycon/GEDICHT_GUNTER EDIT entity OF https://raw.githubusercontent.com/proycon/folia/master/setdefinitions/namedentities.foliaset.xml WITH class loc FOR GEDICHT_GUNTER.p.13.s.1.w.7")


