<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis hasScaleBasedVisibilityFlag="1" styleCategories="AllStyleCategories" labelsEnabled="1" simplifyLocal="1" simplifyAlgorithm="0" minScale="1e+8" readOnly="0" maxScale="0" simplifyDrawingTol="1" version="3.4.12-Madeira" simplifyDrawingHints="1" simplifyMaxScale="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 forceraster="0" symbollevels="0" enableorderby="0" type="singleSymbol">
    <symbols>
      <symbol name="0" alpha="1" type="fill" clip_to_extent="1" force_rhr="0">
        <layer enabled="1" class="LinePatternFill" pass="0" locked="0">
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
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="lineAngle" type="Map">
                  <Option name="active" type="bool" value="false"/>
                  <Option name="field" type="QString" value="azimuthDegre"/>
                  <Option name="type" type="int" value="2"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol name="@0@0" alpha="1" type="line" clip_to_extent="1" force_rhr="0">
            <layer enabled="1" class="SimpleLine" pass="0" locked="0">
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
                  <Option name="name" type="QString" value=""/>
                  <Option name="properties"/>
                  <Option name="type" type="QString" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
        <layer enabled="1" class="SimpleFill" pass="0" locked="0">
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="55,126,184,255" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="207,33,123,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.66" k="outline_width"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="no" k="style"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
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
      <text-style namedStyle="Regular" textOpacity="1" useSubstitutions="0" fontWeight="50" fontWordSpacing="0" multilineHeight="1" blendMode="0" fontLetterSpacing="0" fontCapitals="0" fontSizeUnit="Point" fontItalic="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" isExpression="1" previewBkgrdColor="#ffffff" fieldName=" concat(   &quot;IdRang&quot;  , ' -- précision ',  round(&quot;MAX_hrms&quot;*100 ,1), ' cm - ', round( &quot;azimuthDegre&quot;,1), '° - ',  round(&quot;distance&quot;,1) , ' m - Troncons : ', &quot;IdTroncon&quot; )" fontFamily="Ubuntu" fontUnderline="0" fontStrikeout="0" fontSize="10" textColor="0,0,0,255">
        <text-buffer bufferColor="187,228,24,255" bufferSizeUnits="MM" bufferNoFill="1" bufferJoinStyle="128" bufferSize="1" bufferDraw="1" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferBlendMode="0" bufferOpacity="1"/>
        <background shapeRotation="0" shapeOpacity="1" shapeOffsetUnit="MM" shapeBorderWidth="0" shapeRadiiUnit="MM" shapeBlendMode="0" shapeSVGFile="" shapeRotationType="0" shapeBorderColor="128,128,128,255" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeType="0" shapeFillColor="255,255,255,255" shapeSizeUnit="MM" shapeSizeType="0" shapeOffsetX="0" shapeOffsetY="0" shapeRadiiX="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiY="0" shapeJoinStyle="64" shapeBorderWidthUnit="MM" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeDraw="0" shapeSizeX="0" shapeSizeY="0"/>
        <shadow shadowOffsetDist="1" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowRadiusUnit="MM" shadowOpacity="0.7" shadowOffsetUnit="MM" shadowUnder="0" shadowDraw="0" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetAngle="135" shadowColor="0,0,0,255" shadowRadiusAlphaOnly="0" shadowRadius="1.5" shadowScale="100" shadowOffsetGlobal="1" shadowBlendMode="6"/>
        <substitutions/>
      </text-style>
      <text-format multilineAlign="4294967295" formatNumbers="0" decimals="3" wrapChar="" placeDirectionSymbol="0" autoWrapLength="0" rightDirectionSymbol=">" useMaxLineLengthForAutoWrap="1" reverseDirectionSymbol="0" addDirectionSymbol="0" plussign="0" leftDirectionSymbol="&lt;"/>
      <placement repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" repeatDistanceUnits="MM" dist="0" centroidInside="0" repeatDistance="0" placement="0" maxCurvedCharAngleOut="-25" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" priority="5" centroidWhole="0" placementFlags="10" yOffset="0" preserveRotation="1" distUnits="MM" distMapUnitScale="3x:0,0,0,0,0,0" offsetUnits="MM" xOffset="0" rotationAngle="0" offsetType="0" fitInPolygonOnly="0" quadOffset="4" maxCurvedCharAngleIn="25" labelOffsetMapUnitScale="3x:0,0,0,0,0,0"/>
      <rendering upsidedownLabels="0" obstacleType="0" fontLimitPixelSize="0" obstacleFactor="1" scaleMax="0" displayAll="0" obstacle="1" drawLabels="1" maxNumLabels="2000" labelPerPart="0" scaleMin="0" minFeatureSize="0" fontMaxPixelSize="10000" scaleVisibility="0" fontMinPixelSize="3" zIndex="0" limitNumLabels="0" mergeLines="0"/>
      <dd_properties>
        <Option type="Map">
          <Option name="name" type="QString" value=""/>
          <Option name="properties" type="Map">
            <Option name="LabelRotation" type="Map">
              <Option name="active" type="bool" value="true"/>
              <Option name="field" type="QString" value="orientation"/>
              <Option name="type" type="int" value="2"/>
            </Option>
          </Option>
          <Option name="type" type="QString" value="collection"/>
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
  <SingleCategoryDiagramRenderer diagramType="Histogram" attributeLegend="1">
    <DiagramCategory opacity="1" penWidth="0" scaleDependency="Area" labelPlacementMethod="XHeight" diagramOrientation="Up" height="15" barWidth="5" minimumSize="0" penColor="#000000" penAlpha="255" lineSizeScale="3x:0,0,0,0,0,0" backgroundColor="#ffffff" scaleBasedVisibility="0" minScaleDenominator="0" backgroundAlpha="255" sizeScale="3x:0,0,0,0,0,0" maxScaleDenominator="1e+8" enabled="0" sizeType="MM" lineSizeType="MM" width="15" rotationOffset="270">
      <fontProperties style="" description="Ubuntu,11,-1,5,50,0,0,0,0,0"/>
      <attribute label="" field="" color="#000000"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings dist="0" priority="0" obstacle="0" placement="1" zIndex="0" linePlacementFlags="18" showAll="1">
    <properties>
      <Option type="Map">
        <Option name="name" type="QString" value=""/>
        <Option name="properties"/>
        <Option name="type" type="QString" value="collection"/>
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
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="" field="IdRang" applyOnUpdate="0"/>
    <default expression="" field="IdTroncon" applyOnUpdate="0"/>
    <default expression="" field="largeur" applyOnUpdate="0"/>
    <default expression="" field="MAX_hrms" applyOnUpdate="0"/>
    <default expression="" field="nom" applyOnUpdate="0"/>
    <default expression="" field="distance" applyOnUpdate="0"/>
    <default expression="" field="azimuthDegre" applyOnUpdate="0"/>
    <default expression="" field="orientation" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint notnull_strength="0" constraints="0" field="IdRang" unique_strength="0" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" field="IdTroncon" unique_strength="0" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" field="largeur" unique_strength="0" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" field="MAX_hrms" unique_strength="0" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" field="nom" unique_strength="0" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" field="distance" unique_strength="0" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" field="azimuthDegre" unique_strength="0" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" field="orientation" unique_strength="0" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="IdRang" desc=""/>
    <constraint exp="" field="IdTroncon" desc=""/>
    <constraint exp="" field="largeur" desc=""/>
    <constraint exp="" field="MAX_hrms" desc=""/>
    <constraint exp="" field="nom" desc=""/>
    <constraint exp="" field="distance" desc=""/>
    <constraint exp="" field="azimuthDegre" desc=""/>
    <constraint exp="" field="orientation" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" sortExpression="" actionWidgetStyle="dropDown">
    <columns>
      <column name="nom" hidden="0" type="field" width="-1"/>
      <column hidden="1" type="actions" width="-1"/>
      <column name="azimuthDegre" hidden="0" type="field" width="-1"/>
      <column name="orientation" hidden="0" type="field" width="-1"/>
      <column name="IdRang" hidden="0" type="field" width="-1"/>
      <column name="IdTroncon" hidden="0" type="field" width="-1"/>
      <column name="largeur" hidden="0" type="field" width="-1"/>
      <column name="distance" hidden="0" type="field" width="-1"/>
      <column name="MAX_hrms" hidden="0" type="field" width="-1"/>
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
    <field name="distance" editable="1"/>
    <field name="hrms" editable="1"/>
    <field name="largeur" editable="1"/>
    <field name="nom" editable="1"/>
    <field name="nombreRangs" editable="1"/>
    <field name="orientation" editable="1"/>
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
    <field name="distance" labelOnTop="0"/>
    <field name="hrms" labelOnTop="0"/>
    <field name="largeur" labelOnTop="0"/>
    <field name="nom" labelOnTop="0"/>
    <field name="nombreRangs" labelOnTop="0"/>
    <field name="orientation" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>nombreRangs</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>
