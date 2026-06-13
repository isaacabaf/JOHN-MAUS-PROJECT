<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0">
  <xsl:output method="html" encoding="UTF-8" indent="yes"/>
  <xsl:template match="/">
    <html lang="en"><head><meta charset="UTF-8"/><title>John Maus TEI Output</title>
      <style>body{font-family:Arial,sans-serif;background:#f4f4f4;color:#222;padding:40px}main{max-width:1100px;margin:auto;background:white;padding:40px;border-radius:16px;box-shadow:0 8px 28px rgba(0,0,0,.08)}h1,h2,h3{color:#173f5f}p{font-size:18px;line-height:1.75}.tag{background:#eef6ff;border-bottom:2px solid #173f5f;padding:1px 4px;border-radius:4px}table{width:100%;border-collapse:collapse;margin:18px 0 32px;font-size:14px}th{background:#173f5f;color:white}th,td{border:1px solid #ccc;padding:10px;text-align:left;vertical-align:top}</style>
    </head><body><main>
      <h1><xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title"/></h1>
      <p><strong>Encoded by: </strong><xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:author"/></p>
      <h2>Encoded Text</h2>
      <xsl:for-each select="tei:TEI/tei:text/tei:body/tei:div">
        <h3><xsl:value-of select="tei:head"/></h3>
        <p><xsl:apply-templates select="tei:p/node()"/></p>
      </xsl:for-each>
      <h2>People</h2><table><tr><th>ID</th><th>Name</th><th>Authority</th></tr><xsl:for-each select="tei:TEI/tei:standOff/tei:listPerson/tei:person"><tr><td><xsl:value-of select="@xml:id"/></td><td><xsl:value-of select="tei:persName"/></td><td><xsl:for-each select="tei:idno"><xsl:value-of select="@type"/>: <xsl:value-of select="."/><br/></xsl:for-each></td></tr></xsl:for-each></table>
      <h2>Organizations</h2><table><tr><th>ID</th><th>Name</th><th>Authority</th></tr><xsl:for-each select="tei:TEI/tei:standOff/tei:listOrg/tei:org"><tr><td><xsl:value-of select="@xml:id"/></td><td><xsl:value-of select="tei:orgName"/></td><td><xsl:for-each select="tei:idno"><xsl:value-of select="@type"/>: <xsl:value-of select="."/><br/></xsl:for-each></td></tr></xsl:for-each></table>
      <h2>Places</h2><table><tr><th>ID</th><th>Name</th><th>Authority</th></tr><xsl:for-each select="tei:TEI/tei:standOff/tei:listPlace/tei:place"><tr><td><xsl:value-of select="@xml:id"/></td><td><xsl:value-of select="tei:placeName"/></td><td><xsl:for-each select="tei:idno"><xsl:value-of select="@type"/>: <xsl:value-of select="."/><br/></xsl:for-each></td></tr></xsl:for-each></table>
      <h2>Albums and Textual References</h2><table><tr><th>ID</th><th>Title</th><th>Author</th><th>Date</th></tr><xsl:for-each select="tei:TEI/tei:standOff/tei:listBibl/tei:bibl"><tr><td><xsl:value-of select="@xml:id"/></td><td><xsl:value-of select="tei:title"/></td><td><xsl:value-of select="tei:author"/></td><td><xsl:value-of select="tei:date"/></td></tr></xsl:for-each></table>
      <h2>Relations</h2><table><tr><th>ID</th><th>Relation</th><th>Active</th><th>Passive</th></tr><xsl:for-each select="tei:TEI/tei:standOff/tei:listRelation/tei:relation"><tr><td><xsl:value-of select="@xml:id"/></td><td><xsl:value-of select="@name"/></td><td><xsl:value-of select="@active"/></td><td><xsl:value-of select="@passive"/></td></tr></xsl:for-each></table>
    </main></body></html>
  </xsl:template>
  <xsl:template match="tei:persName|tei:placeName|tei:orgName|tei:term|tei:title|tei:quote"><span class="tag"><xsl:apply-templates/></span></xsl:template>
</xsl:stylesheet>
