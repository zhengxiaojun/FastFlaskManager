# _*_encoding:utf-8_*_

# ===minidom操作XML代码示例
import xml
from xml.dom import minidom
import codecs


# ==由于minidom默认的writexml()函数在读取一个xml文件后，修改后重新写入如果加了newl='\n',会将原有的xml中写入多余的行
# 　 ==因此使用下面这个函数来代替
def fixed_writexml(self, writer, indent="", addindent="", newl=""):
    # indent = current indentation
    # addindent = indentation to add to higher levels
    # newl = newline string
    writer.write(indent + "<" + self.tagName)

    attrs = self._get_attributes()
    a_names = attrs.keys()
    a_names.sort()

    for a_name in a_names:
        writer.write(" %s=\"" % a_name)
        minidom._write_data(writer, attrs[a_name].value)
        writer.write("\"")
    if self.childNodes:
        if len(self.childNodes) == 1 \
                and self.childNodes[0].nodeType == minidom.Node.TEXT_NODE:
            writer.write(">")
            self.childNodes[0].writexml(writer, "", "", "")
            writer.write("</%s>%s" % (self.tagName, newl))
            return
        writer.write(">%s" % (newl))
        for node in self.childNodes:
            if node.nodeType is not minidom.Node.TEXT_NODE:
                node.writexml(writer, indent + addindent, addindent, newl)
        writer.write("%s</%s>%s" % (indent, self.tagName, newl))
    else:
        writer.write("/>%s" % (newl))


minidom.Element.writexml = fixed_writexml


def opXml():
    # # =====从一个空xml文档开始
    impl = xml.dom.getDOMImplementation()
    dom = impl.createDocument(None, 'All_Students', None)
    root = dom.documentElement
    # # --创建一个节点，并添加到root下
    student = dom.createElement('student')
    root.appendChild(student)
    # # --创建一个子节点，并设置属性
    nameE = dom.createElement('name')
    value = u'陈奕迅'
    nameE.setAttribute("attr", value)
    nameN = dom.createTextNode(value)
    nameE.appendChild(nameN)
    student.appendChild(nameE)

    # -- 写进文件,如果出现了unicode，指定文件的编码
    f = codecs.open('1.xml', 'w', 'utf-8')
    dom.writexml(f, addindent='  ', newl='\n', encoding='utf-8')
    f.close()

    # =====处理一个已经存在的xml文档
    dom = xml.dom.minidom.parse("1.xml")
    root = dom.documentElement
    #  -- 重新设置属性
    # --- 返回所有node name为student的节点
    allnodes = dom.getElementsByTagName('student')
    value = u'王力宏'
    for node in allnodes:
        node.setAttribute('name', value)
    # --删除节点属性
    for node in allnodes:
        node.removeAttribute('name')
        # --每个节点有 nodeType,nodeName,和nodeVaulue 等属性
        # --对于textNode，想得到它的文本内容可以使用: .data属性
        print node.nodeType, node.nodeValue
        # --也可以删除节点
        root.removeChild(node)
    f = codecs.open('1.xml', 'w', 'utf-8')
    dom.writexml(f, addindent='  ', newl='\n', encoding='utf-8')
    f.close()


def format_xml(data):
    dom = xml.dom.minidom.parseString(data)
    return dom.toprettyxml(indent='  ', newl='\n', encoding='utf-8')


if __name__ == '__main__':
    # opXml()
    data = '<productList><product><brand_code>1360</brand_code><brand_name>&#28459;&#27493;&#32773;(EDIFIER)</brand_name><categ1_id>157122</categ1_id><categ1_name>&#30005;&#33041;/&#21150;&#20844;/&#22806;&#35774;</categ1_name><categ2_id>157237</categ2_id><categ2_name>&#30005;&#33041;&#22806;&#35774;</categ2_name><categ3_id>157243</categ3_id><categ3_name>&#30005;&#33041;&#38899;&#31665;</categ3_name><categ4_id></categ4_id><categ4_name></categ4_name><categ_id>157243</categ_id><categ_level>3</categ_level><categ_name>&#30005;&#33041;&#38899;&#31665;</categ_name><categ_url></categ_url><click_url>http://product.suning.com/0070072458/100116925.html</click_url><img_url>http://image5.suning.cn/uimg/b2c/newcatentries/0070072458-000000000100116925_1_200x200.jpg</img_url><market_price_1>369.00</market_price_1><price_1>369.00</price_1><biz_code_1>0070070272</biz_code_1><market_price_2>369.00</market_price_2><price_2>369.00</price_2><biz_code_2>0070070272</biz_code_2><shelve_status>1</shelve_status><shelve_status_app>1</shelve_status_app><sku_id>000000000100116925</sku_id><sku_name>&#28459;&#27493;&#32773;&#38899;&#31665;E3100</sku_name><timestamp>1504388958000</timestamp></product><product><brand_code>6418</brand_code><brand_name>&#27801;&#23459;(VS SASSOON)</brand_name><categ1_id>315587</categ1_id><categ1_name>&#32654;&#21457; &#26579;&#28907; &#21475;&#33108;</categ1_name><categ2_id>316546</categ2_id><categ2_name>&#27927;&#25252;&#21457;</categ2_name><categ3_id>336038</categ3_id><categ3_name>&#21457;&#33180;</categ3_name><categ4_id></categ4_id><categ4_name></categ4_name><categ_id>336038</categ_id><categ_level>3</categ_level><categ_name>&#21457;&#33180;</categ_name><categ_url></categ_url><click_url>http://product.suning.com/0070082497/101317192.html</click_url><img_url>http://image1.suning.cn/uimg/b2c/newcatentries/0070082497-000000000101317192_1_200x200.jpg</img_url><market_price_1>54.90</market_price_1><price_1>54.90</price_1><biz_code_1>0000000000</biz_code_1><market_price_2>54.90</market_price_2><price_2>54.90</price_2><biz_code_2>0000000000</biz_code_2><shelve_status>1</shelve_status><shelve_status_app>1</shelve_status_app><sku_id>000000000101317192</sku_id><sku_name>&#27801;&#23459;&#20462;&#25252;&#27700;&#20859;&#21457;&#36136;&#37325;&#22609;&#21457;&#33180;(150ml)</sku_name><timestamp>1505463801000</timestamp></product><product><brand_code>1360</brand_code><brand_name>&#28459;&#27493;&#32773;(EDIFIER)</brand_name><categ1_id>157122</categ1_id><categ1_name>&#30005;&#33041;/&#21150;&#20844;/&#22806;&#35774;</categ1_name><categ2_id>157237</categ2_id><categ2_name>&#30005;&#33041;&#22806;&#35774;</categ2_name><categ3_id>157243</categ3_id><categ3_name>&#30005;&#33041;&#38899;&#31665;</categ3_name><categ4_id></categ4_id><categ4_name></categ4_name><categ_id>157243</categ_id><categ_level>3</categ_level><categ_name>&#30005;&#33041;&#38899;&#31665;</categ_name><categ_url></categ_url><click_url>http://product.suning.com/0070066205/101328226.html</click_url><img_url>http://image4.suning.cn/uimg/b2c/newcatentries/0070066205-000000000101328226_1_200x200.jpg</img_url><market_price_1>339.00</market_price_1><price_1>339.00</price_1><biz_code_1>0070072458</biz_code_1><market_price_2>339.00</market_price_2><price_2>339.00</price_2><biz_code_2>0070072458</biz_code_2><shelve_status>1</shelve_status><shelve_status_app>1</shelve_status_app><sku_id>000000000101328226</sku_id><sku_name>&#28459;&#27493;&#32773;&#65288;EDIFIER&#65289; E3100 2.1&#22768;&#36947; &#22810;&#23186;&#20307;&#38899;&#31665; &#38899;&#21709; &#30005;&#33041;&#38899;&#31665; &#40657;&#33394;</sku_name><timestamp>1504580103680</timestamp></product></productList>'

    print format_xml(data)
