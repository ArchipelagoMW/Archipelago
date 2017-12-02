<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0"
            xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
            xmlns:msxsl="urn:schemas-microsoft-com:xslt"
            exclude-result-prefixes="msxsl"
            xmlns:wix="http://schemas.microsoft.com/wix/2006/wi">

  <xsl:output method="xml" indent="no"/>

  <xsl:strip-space elements="*"/>

  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="wix:File[@Source='SourceDir\EntranceRandomizer.exe']">
      <xsl:copy-of select="." />
      <wix:Shortcut Id="ProgramShortcut"
               Name="ALttP Entrance Randomizer"
               Advertise="yes"
               Description="ALttP Entrance Randomizer"
               Directory="ApplicationProgramsFolder" />
    </xsl:template>
    <xsl:template match="wix:File[@Source='SourceDir\README.hmtl']">
        <xsl:copy-of select="." />
        <wix:Shortcut Id="ReadmeShortcut"
                 Name="ALttP Entrance Randomizer README"
                 Advertise="yes"
                 Description="ALttP Entrance Randomizer README"
                 Directory="ApplicationProgramsFolder" />
      </xsl:template>

</xsl:stylesheet>
