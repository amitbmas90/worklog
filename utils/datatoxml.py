import re
try:
    from lxml import etree
    #print("running with lxml.etree")
except ImportError:
    try:
        # Python 2.5
        import xml.etree.cElementTree as etree
        #print("running with cElementTree on Python 2.5+")
    except ImportError:
        try:
            # Python 2.5
            import xml.etree.ElementTree as etree
            #print("running with ElementTree on Python 2.5+")
        except ImportError:
            try:
                # normal cElementTree install
                import cElementTree as etree
                #print("running with cElementTree")
            except ImportError:
                try:
                    # normal ElementTree install
                    import elementtree.ElementTree as etree
                    #print("running with ElementTree")
                except ImportError:
                    raise ImportError(
                  "Failed to import ElementTree from any known place")
                    
                    
def dict_to_xml(dict_, root_node_tagname="Result"):
    root = etree.Element(root_node_tagname)
    assert isinstance(dict_, dict)
    _append_dict(root, dict_)
    return etree.tostring(root, pretty_print=True)

def list_to_xml(list_, key, root_node_tagname="Result"):
    root = etree.Element(root_node_tagname)
    assert isinstance(list_, (list, tuple))
    _append_list(root, key, list_)
    return etree.tostring(root, pretty_print=True)
            
def _append_dict(root, data):
    for key, value in data.items():
        element = etree.SubElement(root, key)
        if isinstance(value, dict):
            _append_dict(element, value)
        elif isinstance(value, list):
            list_key = re.sub('ies$', '', key)
            if list_key == key:
                list_key = re.sub('s$', '', key)
            if list_key == key:
                list_key += '_item'

            _append_list(element, list_key, value)
        else:
            _append_value(element, value)

def _append_list(element, key, value):
    for v in value:
        sub_element = etree.SubElement(element, key)
        if isinstance(v, dict):
            _append_dict(sub_element, v)
        else:
            _append_value(sub_element, v)
                
def _append_value(element, value):
    if value is not None:
        if isinstance(value, bool):
            value = value and 'true' or 'false'
        #element.set('type', str(type(value)))
        element.text = unicode(value)
    
