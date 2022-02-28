<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyLocal="1" simplifyAlgorithm="0" styleCategories="AllStyleCategories" minScale="1e+8" simplifyMaxScale="1" maxScale="0" readOnly="0" simplifyDrawingHints="1" hasScaleBasedVisibilityFlag="1" simplifyDrawingTol="1" version="3.4.12-Madeira" labelsEnabled="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 symbollevels="0" enableorderby="0" forceraster="0" type="singleSymbol">
    <symbols>
      <symbol clip_to_extent="1" name="0" alpha="1" force_rhr="0" type="fill">
        <layer enabled="1" class="LinePatternFill" locked="0" pass="0">
          <prop v="90" k="angle"/>
          <prop v="55,126,184,255" k="color"/>
          <prop v="10" k="distance"/>
          <prop v="3x:0,0,0,0,0,0" k="distance_map_unit_scale"/>
          <prop v="RenderMetersInMapUnits" k="distance_unit"/>
          <prop v="0.26" k="line_width"/>
          <prop v="3x:0,0,0,0,0,0" k="line_width_map_unit_scale"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="lineAngle" type="Map">
                  <Option name="active" value="false" type="bool"/>
                  <Option name="field" value="azimuthDegre" type="QString"/>
                  <Option name="type" value="2" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol clip_to_extent="1" name="@0@0" alpha="1" force_rhr="0" type="line">
            <layer enabled="1" class="SimpleLine" locked="0" pass="0">
              <prop v="square" k="capstyle"/>
              <prop v="5;2" k="customdash"/>
              <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
              <prop v="MM" k="customdash_unit"/>
              <prop v="0" k="draw_inside_polygon"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="0,0,0,255" k="line_color"/>
              <prop v="solid" k="line_style"/>
              <prop v="0.66" k="line_width"/>
              <prop v="MM" k="line_width_unit"/>
              <prop v="0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="0" k="ring_filter"/>
              <prop v="0" k="use_custom_dash"/>
              <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" value="" type="QString"/>
                  <Option name="properties"/>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
        <layer enabled="1" class="SimpleFill" locked="0" pass="0">
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="255,127,0,255" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="255,127,0,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.66" k="outline_width"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="horizontal" k="style"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <labeling type="simple">
    <settings>
      <text-style fontSizeMapUnitScale="3x:0,0,0,0,0,0" previewBkgrdColor="#ffffff" textColor="0,0,0,255" useSubstitutions="0" fontItalic="0" fontSizeUnit="Point" fontFamily="Ubuntu" fontCapitals="0" fontWordSpacing="0" fontSize="10" textOpacity="1" blendMode="0" namedStyle="Regular" fontLetterSpacing="0" fontUnderline="0" isExpression="1" fontWeight="50" fontStrikeout="0" multilineHeight="1" fieldName=" concat(   &quot;IdRang&quot;  , ' - Alignement ', &quot;ratio50Qualité&quot;   , ' ',    &quot;ratio50Distance&quot;, ' vs50', ' -- précision ',  round(&quot;MAX_hrms&quot;*100 ,1), ' cm - Représentativité ',   &quot;couvertureQualité&quot; , ' ',  round(&quot;couvertureDistance&quot;,1) , ' % - ', round( &quot;azimuthDegre&quot;,1), '° - ',  round(&quot;distance&quot;,1) , ' m - Troncons : ', &quot;IdTroncon&quot;, '  ',  round(&quot;vitesse&quot; ,1) , ' km/h')">
        <text-buffer bufferSizeUnits="MM" bufferNoFill="1" bufferJoinStyle="128" bufferSize="1" bufferDraw="1" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferColor="255,127,0,255" bufferOpacity="1" bufferBlendMode="0"/>
        <background shapeDraw="0" shapeRotation="0" shapeBorderWidthUnit="MM" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeOpacity="1" shapeRadiiUnit="MM" shapeRadiiX="0" shapeRadiiY="0" shapeBorderWidth="0" shapeBlendMode="0" shapeOffsetUnit="MM" shapeSVGFile="" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeType="0" shapeSizeUnit="MM" shapeSizeType="0" shapeFillColor="255,255,255,255" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeBorderColor="128,128,128,255" shapeOffsetX="0" shapeSizeX="0" shapeOffsetY="0" shapeSizeY="0" shapeRotationType="0" shapeJoinStyle="64" shapeSizeMapUnitScale="3x:0,0,0,0,0,0"/>
        <shadow shadowUnder="0" shadowRadius="1.5" shadowRadiusAlphaOnly="0" shadowBlendMode="6" shadowOpacity="0.7" shadowColor="0,0,0,255" shadowOffsetAngle="135" shadowOffsetDist="1" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowScale="100" shadowDraw="0" shadowRadiusUnit="MM" shadowOffsetGlobal="1" shadowOffsetUnit="MM" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0"/>
        <substitutions/>
      </text-style>
      <text-format decimals="3" rightDirectionSymbol=">" wrapChar="" useMaxLineLengthForAutoWrap="1" multilineAlign="4294967295" leftDirectionSymbol="&lt;" reverseDirectionSymbol="0" plussign="0" addDirectionSymbol="0" autoWrapLength="0" placeDirectionSymbol="0" formatNumbers="0"/>
      <placement fitInPolygonOnly="0" maxCurvedCharAngleOut="-25" maxCurvedCharAngleIn="25" offsetUnits="MM" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" centroidInside="0" repeatDistance="0" dist="0" placement="0" priority="5" centroidWhole="0" repeatDistanceUnits="MM" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" placementFlags="10" offsetType="0" quadOffset="4" rotationAngle="0" preserveRotation="1" distMapUnitScale="3x:0,0,0,0,0,0" distUnits="MM" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" yOffset="0" xOffset="0"/>
      <rendering fontLimitPixelSize="0" fontMinPixelSize="3" scaleVisibility="0" scaleMax="0" obstacleFactor="1" upsidedownLabels="0" drawLabels="1" maxNumLabels="2000" zIndex="0" scaleMin="0" mergeLines="0" labelPerPart="0" minFeatureSize="0" fontMaxPixelSize="10000" limitNumLabels="0" obstacleType="0" obstacle="1" displayAll="0"/>
      <dd_properties>
        <Option type="Map">
          <Option name="name" value="" type="QString"/>
          <Option name="properties" type="Map">
            <Option name="LabelRotation" type="Map">
              <Option name="active" value="true" type="bool"/>
              <Option name="field" value="orientation" type="QString"/>
              <Option name="type" value="2" type="int"/>
            </Option>
          </Option>
          <Option name="type" value="collection" type="QString"/>
        </Option>
      </dd_properties>
    </settings>
  </labeling>
  <customproperties>
    <property key="dualview/previewExpressions" value="nombreRangs"/>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory maxScaleDenominator="1e+8" penColor="#000000" penAlpha="255" enabled="0" barWidth="5" labelPlacementMethod="XHeight" lineSizeScale="3x:0,0,0,0,0,0" sizeType="MM" scaleDependency="Area" opacity="1" height="15" lineSizeType="MM" width="15" penWidth="0" scaleBasedVisibility="0" backgroundColor="#ffffff" backgroundAlpha="255" minimumSize="0" rotationOffset="270" sizeScale="3x:0,0,0,0,0,0" minScaleDenominator="0" diagramOrientation="Up">
      <fontProperties description="Ubuntu,11,-1,5,50,0,0,0,0,0" style=""/>
      <attribute label="" field="" color="#000000"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings priority="0" obstacle="0" zIndex="0" dist="0" placement="1" linePlacementFlags="18" showAll="1">
    <properties>
      <Option type="Map">
        <Option name="name" value="" type="QString"/>
        <Option name="properties"/>
        <Option name="type" value="collection" type="QString"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="IdRang">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="IdTroncon">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="largeur">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="MAX_hrms">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="nom">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="distance">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="azimuthDegre">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="orientation">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="vitesse">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="sensAvancement">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="couvertureQualité">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="couvertureDistance">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="ratio50Distance">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="ratio50Qualité">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" field="IdRang" index="0"/>
    <alias name="" field="IdTroncon" index="1"/>
    <alias name="" field="largeur" index="2"/>
    <alias name="" field="MAX_hrms" index="3"/>
    <alias name="" field="nom" index="4"/>
    <alias name="" field="distance" index="5"/>
    <alias name="" field="azimuthDegre" index="6"/>
    <alias name="" field="orientation" index="7"/>
    <alias name="" field="vitesse" index="8"/>
    <alias name="" field="sensAvancement" index="9"/>
    <alias name="" field="couvertureQualité" index="10"/>
    <alias name="" field="couvertureDistance" index="11"/>
    <alias name="" field="ratio50Distance" index="12"/>
    <alias name="" field="ratio50Qualité" index="13"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="" applyOnUpdate="0" field="IdRang"/>
    <default expression="" applyOnUpdate="0" field="IdTroncon"/>
    <default expression="" applyOnUpdate="0" field="largeur"/>
    <default expression="" applyOnUpdate="0" field="MAX_hrms"/>
    <default expression="" applyOnUpdate="0" field="nom"/>
    <default expression="" applyOnUpdate="0" field="distance"/>
    <default expression="" applyOnUpdate="0" field="azimuthDegre"/>
    <default expression="" applyOnUpdate="0" field="orientation"/>
    <default expression="" applyOnUpdate="0" field="vitesse"/>
    <default expression="" applyOnUpdate="0" field="sensAvancement"/>
    <default expression="" applyOnUpdate="0" field="couvertureQualité"/>
    <default expression="" applyOnUpdate="0" field="couvertureDistance"/>
    <default expression="" applyOnUpdate="0" field="ratio50Distance"/>
    <default expression="" applyOnUpdate="0" field="ratio50Qualité"/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="IdRang" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="IdTroncon" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="largeur" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="MAX_hrms" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="nom" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="distance" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="azimuthDegre" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="orientation" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="vitesse" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="sensAvancement" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="couvertureQualité" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="couvertureDistance" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="ratio50Distance" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="ratio50Qualité" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" field="IdRang" exp=""/>
    <constraint desc="" field="IdTroncon" exp=""/>
    <constraint desc="" field="largeur" exp=""/>
    <constraint desc="" field="MAX_hrms" exp=""/>
    <constraint desc="" field="nom" exp=""/>
    <constraint desc="" field="distance" exp=""/>
    <constraint desc="" field="azimuthDegre" exp=""/>
    <constraint desc="" field="orientation" exp=""/>
    <constraint desc="" field="vitesse" exp=""/>
    <constraint desc="" field="sensAvancement" exp=""/>
    <constraint desc="" field="couvertureQualité" exp=""/>
    <constraint desc="" field="couvertureDistance" exp=""/>
    <constraint desc="" field="ratio50Distance" exp=""/>
    <constraint desc="" field="ratio50Qualité" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" actionWidgetStyle="dropDown" sortExpression="">
    <columns>
      <column width="-1" hidden="0" name="nom" type="field"/>
      <column width="-1" hidden="1" type="actions"/>
      <column width="-1" hidden="0" name="azimuthDegre" type="field"/>
      <column width="-1" hidden="0" name="orientation" type="field"/>
      <column width="-1" hidden="0" name="IdRang" type="field"/>
      <column width="-1" hidden="0" name="IdTroncon" type="field"/>
      <column width="-1" hidden="0" name="largeur" type="field"/>
      <column width="-1" hidden="0" name="distance" type="field"/>
      <column width="-1" hidden="0" name="MAX_hrms" type="field"/>
      <column width="-1" hidden="0" name="vitesse" type="field"/>
      <column width="-1" hidden="0" name="sensAvancement" type="field"/>
      <column width="-1" hidden="0" name="couvertureQualité" type="field"/>
      <column width="-1" hidden="0" name="couvertureDistance" type="field"/>
      <column width="-1" hidden="0" name="ratio50Distance" type="field"/>
      <column width="-1" hidden="0" name="ratio50Qualité" type="field"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
Les formulaires QGIS peuvent avoir une fonction Python qui sera appelée à l'ouverture du formulaire.

Utilisez cette fonction pour ajouter plus de fonctionnalités à vos formulaires.

Entrez le nom de la fonction dans le champ "Fonction d'initialisation Python".
Voici un exemple à suivre:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
    geom = feature.geometry()
    control = dialog.findChild(QWidget, "MyLineEdit")

]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field name="DATE_capture" editable="1"/>
    <field name="IdPolygone" editable="1"/>
    <field name="IdRang" editable="1"/>
    <field name="IdTroncon" editable="1"/>
    <field name="MAX_ecart" editable="1"/>
    <field name="MAX_ecartement" editable="1"/>
    <field name="MAX_fid" editable="1"/>
    <field name="MAX_hrms" editable="1"/>
    <field name="MIN_fid" editable="1"/>
    <field name="MaxHRMS" editable="1"/>
    <field name="STD_azimuthDegre" editable="1"/>
    <field name="azimuthDegre" editable="1"/>
    <field name="capture" editable="1"/>
    <field name="caster" editable="1"/>
    <field name="couvertureDistance" editable="1"/>
    <field name="couvertureQualité" editable="1"/>
    <field name="distance" editable="1"/>
    <field name="hrms" editable="1"/>
    <field name="largeur" editable="1"/>
    <field name="nom" editable="1"/>
    <field name="nombreRangs" editable="1"/>
    <field name="orientation" editable="1"/>
    <field name="pourcentageCouvert" editable="1"/>
    <field name="qualite" editable="1"/>
    <field name="ratio50Distance" editable="1"/>
    <field name="ratio50Qualité" editable="1"/>
    <field name="sensAvancement" editable="1"/>
    <field name="vitesse" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="DATE_capture" labelOnTop="0"/>
    <field name="IdPolygone" labelOnTop="0"/>
    <field name="IdRang" labelOnTop="0"/>
    <field name="IdTroncon" labelOnTop="0"/>
    <field name="MAX_ecart" labelOnTop="0"/>
    <field name="MAX_ecartement" labelOnTop="0"/>
    <field name="MAX_fid" labelOnTop="0"/>
    <field name="MAX_hrms" labelOnTop="0"/>
    <field name="MIN_fid" labelOnTop="0"/>
    <field name="MaxHRMS" labelOnTop="0"/>
    <field name="STD_azimuthDegre" labelOnTop="0"/>
    <field name="azimuthDegre" labelOnTop="0"/>
    <field name="capture" labelOnTop="0"/>
    <field name="caster" labelOnTop="0"/>
    <field name="couvertureDistance" labelOnTop="0"/>
    <field name="couvertureQualité" labelOnTop="0"/>
    <field name="distance" labelOnTop="0"/>
    <field name="hrms" labelOnTop="0"/>
    <field name="largeur" labelOnTop="0"/>
    <field name="nom" labelOnTop="0"/>
    <field name="nombreRangs" labelOnTop="0"/>
    <field name="orientation" labelOnTop="0"/>
    <field name="pourcentageCouvert" labelOnTop="0"/>
    <field name="qualite" labelOnTop="0"/>
    <field name="ratio50Distance" labelOnTop="0"/>
    <field name="ratio50Qualité" labelOnTop="0"/>
    <field name="sensAvancement" labelOnTop="0"/>
    <field name="vitesse" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>nombreRangs</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>
