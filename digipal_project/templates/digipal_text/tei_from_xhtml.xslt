{% extends "digipal_text/tei_from_xhtml_base.xslt" %}

{% block tei %}

  {{ block.super }}

  <xsl:template name="split_attribute_value">
    <xsl:param name="attribute_value" />
    <xsl:param name="type" />
    <xsl:variable name="new_attribute_value" select="concat(normalize-space($attribute_value), ' ')" />
    <xsl:variable name="first_item" select="substring-before($new_attribute_value, ' ')" />
    <xsl:variable name="following_items" select="substring-after($new_attribute_value, ' ')" />
    <xsl:choose>
      <xsl:when test="$type = 'character' or $type = 'time'">
        <xsl:text>#character-</xsl:text>
      </xsl:when>
      <xsl:when test="$type = 'source'">
        <xsl:text>#source-</xsl:text>
      </xsl:when>
      <xsl:when test="$type = 'place'">
        <xsl:text>#place-</xsl:text>
      </xsl:when>
    </xsl:choose>
    <xsl:value-of select="substring-after($first_item, '#')" />
    <xsl:if test="$following_items">
      <xsl:text> </xsl:text>
    </xsl:if>
    <xsl:if test="$following_items">
      <xsl:call-template name="split_attribute_value">
        <xsl:with-param name="attribute_value" select="$following_items" />
        <xsl:with-param name="type">
          <xsl:choose>
            <xsl:when test="$type = 'place'">
              <xsl:value-of select="'character'" />
            </xsl:when>
            <xsl:otherwise>
              <xsl:value-of select="$type" />
            </xsl:otherwise>
          </xsl:choose>
        </xsl:with-param>
      </xsl:call-template>
    </xsl:if>
  </xsl:template>

  {% block persname %}
  <xsl:template match="span[@data-dpt='persName']">
    <xsl:element name="rs">
      <xsl:attribute name="ref">
        <xsl:text>#character-</xsl:text>
        <xsl:value-of select="substring-after(@data-dpt-ref, '#')" />
      </xsl:attribute>
      <xsl:apply-templates/>
    </xsl:element>
  </xsl:template>
  {% endblock %}

  {% block person %}
  <xsl:template match="span[@data-dpt='rs']">
    <xsl:element name="rs">
      <xsl:attribute name="ref">
        <xsl:call-template name="split_attribute_value">
          <xsl:with-param name="attribute_value" select="@data-dpt-ref" />
          <xsl:with-param name="type" select="'character'" />
        </xsl:call-template>
      </xsl:attribute>
      <xsl:attribute name="ana">
        <xsl:value-of select="@data-dpt-ana" />
      </xsl:attribute>
      <xsl:apply-templates/>
    </xsl:element>
  </xsl:template>
  {% endblock %}

  {% block source %}
  <xsl:template match="span[@data-dpt='quote']">
    <xsl:element name="quote">
      <xsl:if test="@data-dpt-corresp">
        <xsl:attribute name="corresp">
          <xsl:call-template name="split_attribute_value">
            <xsl:with-param name="attribute_value" select="@data-dpt-corresp" />
            <xsl:with-param name="type" select="'source'" />
          </xsl:call-template>
        </xsl:attribute>
      </xsl:if>
      <xsl:attribute name="ana">
        <xsl:value-of select="@data-dpt-ana" />
      </xsl:attribute>
      <xsl:if test="@data-dpt-n">
        <xsl:attribute name="n">
          <xsl:value-of select="@data-dpt-n" />
        </xsl:attribute>
      </xsl:if>
      <xsl:apply-templates/>
    </xsl:element>
  </xsl:template>
  {% endblock %}

  {% block place %}
  <xsl:template match="span[@data-dpt='placeName']">
    <xsl:element name="placeName">
      <xsl:attribute name="ref">
        <xsl:call-template name="split_attribute_value">
          <xsl:with-param name="attribute_value" select="@data-dpt-ref" />
          <xsl:with-param name="type" select="'place'" />
        </xsl:call-template>
      </xsl:attribute>
      <xsl:attribute name="ana">
        <xsl:value-of select="@data-dpt-ana" />
      </xsl:attribute>
      <xsl:apply-templates/>
    </xsl:element>
  </xsl:template>
  {% endblock %}

  {% block time %}
  <xsl:template match="span[@data-dpt='date']">
    <xsl:element name="date">
      <xsl:if test="@data-dpt-ref">
        <xsl:attribute name="ref">
          <xsl:call-template name="split_attribute_value">
            <xsl:with-param name="attribute_value" select="@data-dpt-ref" />
            <xsl:with-param name="type" select="'time'" />
          </xsl:call-template>
        </xsl:attribute>
      </xsl:if>
      <xsl:attribute name="ana">
        <xsl:value-of select="@data-dpt-ana" />
      </xsl:attribute>
      <xsl:apply-templates/>
    </xsl:element>
  </xsl:template>
  {% endblock %}

  {% block interpretation %}
  <xsl:template match="span[@data-dpt='seg']">
    <xsl:element name="seg">
      <xsl:attribute name="ana">
        <xsl:value-of select="@data-dpt-ana" />
      </xsl:attribute>
      <xsl:apply-templates/>
    </xsl:element>
  </xsl:template>
  {% endblock %}

  {% block location_entry %}
  <xsl:template match="span[@data-dpt='location'][@data-dpt-loctype='entry']">
    <xsl:element name="pb">
      <xsl:attribute name="n">
        <xsl:value-of select="text()" />
      </xsl:attribute>
    </xsl:element>
  </xsl:template>
  {% endblock %}

{% endblock %}

{% block header %}
<teiHeader>
  <fileDesc>
    <titleStmt>
      {% block title %}
        <title type="main">{{ meta.title }}</title>
      {% endblock %}
      {% block author %}
        <author>{{ meta.author }}</author>
      {% endblock %}
    </titleStmt>
    <publicationStmt>
      {% if meta.edition %}
        <publisher>{{ meta.edition.publisher }}</publisher>
        <date>{{ meta.edition.date }}</date>
      {% endif %}
      {% if meta.availability %}
        <availability>
          <licence>{{ meta.availability }}</licence>
        </availability>
      {% endif %}
      {% for collaboration in meta.text.collaborations %}
        <respStmt>
          <resp>{{ collaboration.activity.name }}</resp>
          <name>{{ collaboration.collaborator.first_name }} {{ collaboration.collaborator.last_name }}</name>
        </respStmt>
      {% endfor %}
    </publicationStmt>
    <sourceDesc>
      {% if meta.manuscript %}
        <msDesc>
          <msIdentifier>
            <settlement>{{ meta.manuscript.place }}</settlement>
            <repository>{{ meta.manuscript.repository }}</repository>
            <idno>{{ meta.manuscript.shelfmark }}</idno>
          </msIdentifier>
        </msDesc>
      {% endif %}
      {% if meta.edition %}
        <bibl>
          <title>{{ meta.edition.title }}</title>
          <author>{{ meta.edition.author }}</author>
          <editor>{{ meta.edition.editor }}</editor>
          <edition>
            <date>{{ meta.edition.date }}</date>
            <publisher>{{ meta.edition.publisher }}</publisher>
          </edition>
        </bibl>
      {% endif %}
    </sourceDesc>
  </fileDesc>
  <profileDesc>
    {% if meta.text.story_start_date %}
      <settingDesc>
        <setting>
          <time>{{ meta.text.story_start_date }}</time>
        </setting>
      </settingDesc>
    {% endif %}
    <particDesc>
      <listPerson>
        <desc>Characters List</desc>
        {% for character in meta.text.characters %}
          <person xml:id="character-{{ character.id }}">
            <persName>{{ character.name }}</persName>
          </person>
        {% endfor %}
      </listPerson>
    </particDesc>
    <textClass>
      <keywords>
        <term>{{ meta.text.type }}</term>
      </keywords>
    </textClass>
    <textClass>
      <classCode scheme="ann-prosop">
        <interGrp type="status" xml:id="PROS-EV-ST">
          <desc>Status</desc>
          <interp xml:id="PROS-EV-ST-C">Single</interp>
          <interp xml:id="PROS-EV-ST-M">Married</interp>
          <interp xml:id="PROS-EV-ST-V">Widower/Widow</interp>
        </interGrp>
        <interp xml:id="PROS-EV-PHY">Physical Aspect</interp>
        <interGrp type="psychology" xml:id="PROS-EV-PSY">
          <desc>Psychology</desc>
          <interp xml:id="PROS-EV-PSY-BON">Happiness</interp>
          <interp xml:id="PROS-EV-PSY-MAL">Unhappiness</interp>
        </interGrp>
        <interGrp type="socio_economic_status" xml:id="PROS-EV-NSOCIO-EC">
          <desc>Socio Economic Status</desc>
          <interGrp type="status" xml:id="PROS-EV-NSOCIO-EC-S">
            <desc>Status</desc>
            <interp xml:id="PROS-EV-NSOCIO-EC-S-A">Ascension</interp>
            <interp xml:id="PROS-EV-NSOCIO-EC-S-D">Decline</interp>
          </interGrp>
          <interp xml:id="PROS-EV-NSOCIO-EC-HAB">Clothes</interp>
          <interp xml:id="PROS-EV-NSOCIO-EC-HABIT">Building Estate</interp>
          <interp xml:id="PROS-EV-NSOCIO-EC-PROPR">Properties</interp>
        </interGrp>
        <interGrp type="culture" xml:id="PROS-EV-CUL">
          <desc>Culture</desc>
          <interGrp type="language_level" xml:id="PROS-EV-CUL-NLANG">
            <desc>Level of Language</desc>
            <interp xml:id="PROS-EV-CUL-NLANG-H">High Level of Language</interp>
            <interp xml:id="PROS-EV-CUL-NLANG-B">Low Level of Language</interp>
          </interGrp>
        </interGrp>
        <interGrp type="relation" xml:id="PROS-EV-REL">
          <desc>Relation</desc>
          <interp xml:id="PROS-EV-REL-AVEC">Relation With</interp>
          <interGrp type="type" xml:id="PROS-EV-REL-TY">
            <desc>Type</desc>
            <interGrp type="familial" xml:id="PROS-EV-REL-TY-FAM">
              <desc>Familial</desc>
              <interp xml:id="PROS-EV-REL-TY-FAM-ENF">Child</interp>
              <interp xml:id="PROS-EV-REL-TY-FAM-PTSENF">Grandchild</interp>
              <interp xml:id="PROS-EV-REL-TY-FAM-PAR">Parent</interp>
              <interp xml:id="PROS-EV-REL-TY-FAM-GRPAR">Grandparent</interp>
              <interp xml:id="PROS-EV-REL-TY-FAM-ONC">Uncle</interp>
              <interp xml:id="PROS-EV-REL-TY-FAM-TAN">Aunt</interp>
              <interp xml:id="PROS-EV-REL-TY-FAM-NEV">Nephew</interp>
              <interp xml:id="PROS-EV-REL-TY-FAM-NIEC">Niece</interp>
              <interp xml:id="PROS-EV-REL-TY-FAM-FRA">Sibling</interp>
              <interp xml:id="PROS-EV-REL-TY-FAM-MAR">Marriage</interp>
              <interp xml:id="PROS-EV-REL-TY-FAM-PARR">Godparent</interp>
            </interGrp>
            <interGrp type="social" xml:id="PROS-EV-REL-TY-SOC">
              <desc>Social</desc>
              <interGrp type="level" xml:id="PROS-EV-REL-TY-SOC-N">
                <desc>Level</desc>
                <interp xml:id="PROS-EV-REL-TY-SOC-N-AVECI">With an Inferior</interp>
                <interp xml:id="PROS-EV-REL-TY-SOC-N-AVECS">With a Superior</interp>
                <interp xml:id="PROS-EV-REL-TY-SOC-N-AVECP">With an Equal</interp>
              </interGrp>
              <interGrp type="type" xml:id="PROS-EV-REL-TY-SOC-TY">
                <desc>Type</desc>
                <interp xml:id="PROS-EV-REL-TY-SOC-TY-PRO">Professional</interp>
                <interp xml:id="PROS-EV-REL-TY-SOC-TY-INST">Institutional</interp>
                <interp xml:id="PROS-EV-REL-TY-SOC-TY-AMOR">Love</interp>
                <interp xml:id="PROS-EV-REL-TY-SOC-TY-AMIC">Friendship</interp>
                <interp xml:id="PROS-EV-REL-TY-SOC-TY-HOST">Hostility</interp>
              </interGrp>
            </interGrp>
          </interGrp>
        </interGrp>
        <interGrp type="time" xml:id="PROS-CR">
          <desc>Time</desc>
          <interp xml:id="PROS-CR-TR">Real</interp>
          <interp xml:id="PROS-CR-TM">Mythological</interp>
        </interGrp>
        <interGrp type="place" xml:id="PROS-L">
          <desc>Place</desc>
          <interp xml:id="PROS-L-VIL">City</interp>
          <interp xml:id="PROS-L-PAY">Country</interp>
          <interp xml:id="PROS-L-CONT">Continent</interp>
        </interGrp>
      </classCode>
      <classCode scheme="ann-interp">
        <interGrp type="literary_function" xml:id="LIT-FON">
          <desc>Literary Function</desc>
          <interp xml:id="LIT-FON-CONS">Consolation</interp>
          <interGrp type="knowledge" xml:id="LIT-FON-CONN">
            <desc>Knowledge</desc>
            <interp xml:id="LIT-FON-CONN-SOI">Self Awareness</interp>
            <interp xml:id="LIT-FON-CONN-MON">World Knowledge</interp>
          </interGrp>
          <interp xml:id="LIT-FON-DIV">Entertainment</interp>
          <interp xml:id="LIT-FON-THAUM">Thaumaturgic</interp>
          <interp xml:id="LIT-FON-META">Metaliterary</interp>
          <interGrp type="socio_politic" xml:id="LIT-FON-SOCIOPOL">
            <desc>Socio-politic</desc>
            <interp xml:id="LIT-FON-SOCIOPOL-CIV">Civic Function</interp>
            <interp xml:id="LIT-FON-SOCIOPOL-INTERPERS">Interpersonal</interp>
          </interGrp>
        </interGrp>
        <interGrp type="target_audience" xml:id="LIT-PUBL">
          <desc>Target Audience</desc>
          <interGrp type="gender" xml:id="LIT-PUBL-GEN">
            <desc>Gender</desc>
            <interp xml:id="LIT-PUBL-GEN-M">Male</interp>
            <interp xml:id="LIT-PUBL-GEN-F">Female</interp>
          </interGrp>
          <interGrp type="social_status" xml:id="LIT-PUBL-NSOC">
            <desc>Social Status</desc>
            <interp xml:id="LIT-PUBL-NSOC-H">High</interp>
            <interp xml:id="LIT-PUBL-NSOC-B">Low</interp>
          </interGrp>
          <interGrp type="function" xml:id="LIT-PUBL-FON">
            <desc>Function</desc>
            <interp xml:id="LIT-PUBL-FON-EXE">Exegetic</interp>
            <interp xml:id="LIT-PUBL-FON-DID">Didactic</interp>
          </interGrp>
        </interGrp>
        <interGrp type="judgment" xml:id="BOC">
          <desc>Judgment</desc>
          <interp xml:id="BOC-A">Ambiguous</interp>
          <interp xml:id="BOC-P">Positive</interp>
          <interp xml:id="BOC-N">Negative</interp>
          <interp xml:id="BOC-NEU">Neutral</interp>
          <interp xml:id="BOC-IRO">Ironic</interp>
        </interGrp>
      </classCode>
      <classCode scheme="ann-source">
        <interGrp type="direct" xml:id="SOUR-EV">
          <desc>Direct Source</desc>
          <interp xml:id="SOUR-EV-LEX">Lexical</interp>
          <interp xml:id="SOUR-EV-CONT">Content</interp>
          <interp xml:id="SOUR-EV-AUT">Author Name</interp>
          <interp xml:id="SOUR-EV-TIT">Title</interp>
          <interp xml:id="SOUR-EV-AUT-TIT">Author Name and Title</interp>
        </interGrp>
        <interGrp type="indirect" xml:id="SOUR-IND">
          <desc>Indirect Source</desc>
          <interp xml:id="SOUR-IND-LEX">Lexical</interp>
          <interp xml:id="SOUR-IND-CONT">Content</interp>
          <interp xml:id="SOUR-IND-AUT">Author Name</interp>
          <interp xml:id="SOUR-IND-TIT">Title</interp>
          <interp xml:id="SOUR-IND-AUT-TIT">Author Name and Title</interp>
        </interGrp>
      </classCode>
    </textClass>
  </profileDesc>
</teiHeader>
{% endblock %}

{% block text %}
<text>
  <back>
    <listBibl>
      <desc>Sources List</desc>
        {% for source in meta.text.sources %}
          <bibl xml:id="source-{{source.id}}">{{ source.title }}</bibl>
        {% endfor %}
    </listBibl>
    <listPlace>
      <desc>Places List</desc>
      {% for place in meta.text.places %}
        <place xml:id="place-{{ place.id }}">
          <placeName>{{ place.name }}</placeName>
        </place>
      {% endfor %}
    </listPlace>
  </back>
  <body>
    <head>{{ meta.text.title }}</head>
    <div>
      <xsl:apply-templates />
    </div>
  </body>
</text>
{% endblock %}
