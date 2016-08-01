# DXF to webgl translator

Most three.js translators/uploaders import solids in to the three.js format in a "dumb" format. This is a python translator to quickly convert DXF in to an editable three.js format.

See example here - http://harrykeen18.github.io/dxf-three.js-JSON_translator/

Current working directory  - dxf-three.js-JSON_translator\dxf-reader\03_3d_line_to, combines work from all others.

Run gen3_lineto.py with location of chosen dxf file with test polylines as global variable DXFFILE. Scrpit inserts three.js geometry in to a viewable html file "NEW_gen3_linto.html"

02_3d_vector3 outputs parameterised three.js geometry into a text file the content of which can be pasted in to a html doc.
