from pathlib import Path
import xml.etree.ElementTree as ET
import re

TEI_FILE = Path("john_maus_TEI.xml")
RDF_FILE = Path("john_maus_RDF_output.ttl")

NS = {"tei": "http://www.tei-c.org/ns/1.0", "xml": "http://www.w3.org/XML/1998/namespace"}
PREFIXES = '''@prefix ex: <https://johnmaus.com/resource/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix schema: <https://schema.org/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

'''

RELATION_MAP = {
    "bornIn": "schema:birthPlace", "studiedAt": "schema:alumniOf",
    "collaboratedWith": "dcterms:relation", "performedWith": "schema:performer",
    "pastMemberOf": "schema:memberOf", "created": "dcterms:creator",
    "releasedBy": "dcterms:publisher", "titleReference": "dcterms:source",
    "authorOf": "dcterms:creator", "hasGenre": "schema:genre"
}

def xmlid(element):
    return element.attrib.get("{http://www.w3.org/XML/1998/namespace}id", "")

def text(element):
    if element is None:
        return ""
    return " ".join("".join(element.itertext()).split()).replace('"', '\\"')

def uri(value):
    return "ex:" + re.sub(r"[^A-Za-z0-9_]", "", value.replace("#", ""))

root = ET.parse(TEI_FILE).getroot()
triples = [PREFIXES]

for person in root.findall(".//tei:listPerson/tei:person", NS):
    pid = xmlid(person)
    triples += [f"{uri(pid)} a foaf:Person ;", f'  foaf:name "{text(person.find("tei:persName", NS))}" ;']
    for idno in person.findall("tei:idno", NS): triples.append(f"  owl:sameAs <{text(idno)}> ;")
    triples[-1] = triples[-1].rstrip(" ;") + " .\n"

for org in root.findall(".//tei:listOrg/tei:org", NS):
    oid = xmlid(org)
    triples += [f"{uri(oid)} a foaf:Organization ;", f'  foaf:name "{text(org.find("tei:orgName", NS))}" ;']
    for idno in org.findall("tei:idno", NS): triples.append(f"  owl:sameAs <{text(idno)}> ;")
    triples[-1] = triples[-1].rstrip(" ;") + " .\n"

for place in root.findall(".//tei:listPlace/tei:place", NS):
    plid = xmlid(place)
    triples += [f"{uri(plid)} a schema:Place ;", f'  schema:name "{text(place.find("tei:placeName", NS))}" ;']
    for idno in place.findall("tei:idno", NS): triples.append(f"  owl:sameAs <{text(idno)}> ;")
    triples[-1] = triples[-1].rstrip(" ;") + " .\n"

for bibl in root.findall(".//tei:listBibl/tei:bibl", NS):
    bid = xmlid(bibl)
    rdf_type = "dcterms:BibliographicResource" if bid == "fifteenTheses" else "schema:MusicAlbum"
    triples += [f"{uri(bid)} a {rdf_type} ;", f'  schema:name "{text(bibl.find("tei:title", NS))}" ;']
    author = bibl.find("tei:author", NS)
    if author is not None and "ref" in author.attrib: triples.append(f"  dcterms:creator {uri(author.attrib['ref'])} ;")
    date = text(bibl.find("tei:date", NS))
    if date: triples.append(f'  schema:datePublished "{date}" ;')
    for idno in bibl.findall("tei:idno", NS): triples.append(f"  owl:sameAs <{text(idno)}> ;")
    triples[-1] = triples[-1].rstrip(" ;") + " .\n"

for item in root.findall(".//tei:list[@type='concepts']/tei:item", NS):
    triples.append(f'{uri(xmlid(item))} a skos:Concept ; skos:prefLabel "{text(item.find("tei:term", NS))}" .')

for rel in root.findall(".//tei:listRelation/tei:relation", NS):
    triples.append(f"{uri(rel.attrib.get('active',''))} {RELATION_MAP.get(rel.attrib.get('name',''), 'dcterms:relation')} {uri(rel.attrib.get('passive',''))} .")

RDF_FILE.write_text("\n".join(triples), encoding="utf-8")
print(f"Created {RDF_FILE}")
