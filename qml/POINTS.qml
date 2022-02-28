<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis labelsEnabled="1" simplifyLocal="1" simplifyAlgorithm="0" styleCategories="AllStyleCategories" simplifyMaxScale="1" version="3.4.12-Madeira" hasScaleBasedVisibilityFlag="0" simplifyDrawingHints="0" minScale="1e+8" maxScale="0" readOnly="0" simplifyDrawingTol="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 symbollevels="0" enableorderby="0" forceraster="0" type="singleSymbol">
    <symbols>
      <symbol force_rhr="0" name="0" alpha="1" clip_to_extent="1" type="marker">
        <layer enabled="1" class="SimpleMarker" pass="0" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="31,120,180,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="circle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="228,24,24,0"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.2"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="0.7"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MapUnit"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="size" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="field" value="hrms" type="QString"/>
                  <Option name="type" value="2" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer enabled="1" class="SimpleMarker" pass="0" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="228,24,24,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="circle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="253,175,17,0"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.2"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="0.7"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MapUnit"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="size" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="field" value="drms" type="QString"/>
                  <Option name="type" value="2" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer enabled="1" class="SimpleMarker" pass="0" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="205,203,200,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="arrow"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.2"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="3.2"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MapUnit"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="angle" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="field" value="azimuthDegre" type="QString"/>
                  <Option name="type" value="2" type="int"/>
                </Option>
                <Option name="size" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="field" value="drms" type="QString"/>
                  <Option name="type" value="2" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <labeling type="rule-based">
    <rules key="{64041c84-8e52-488c-8bf5-a49bbf1ac26f}">
      <rule filter=" &quot;hrms&quot; > 0.01" description="HRMS supérieur à mm" key="{aeb8af04-2858-4278-bf44-8acdd2102ef2}">
        <settings>
          <text-style multilineHeight="1" namedStyle="Regular" fontSize="10" fontWeight="50" fieldName=" round( hrms*100, 2)" fontUnderline="0" fontSizeUnit="Pixel" fontStrikeout="0" fontCapitals="0" fontLetterSpacing="0" textColor="0,0,0,255" textOpacity="1" isExpression="1" useSubstitutions="0" fontWordSpacing="0" previewBkgrdColor="#ffffff" fontItalic="0" blendMode="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontFamily="Ubuntu">
            <text-buffer bufferOpacity="1" bufferBlendMode="0" bufferSize="2" bufferDraw="1" bufferSizeUnits="MM" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferJoinStyle="128" bufferColor="205,203,200,255" bufferNoFill="1"/>
            <background shapeSizeX="0" shapeSizeY="0" shapeSizeUnit="MM" shapeSizeType="0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiX="0" shapeBorderColor="128,128,128,255" shapeRadiiY="0" shapeSVGFile="" shapeDraw="0" shapeJoinStyle="64" shapeRotationType="0" shapeOffsetUnit="MM" shapeOffsetX="0" shapeRadiiUnit="MM" shapeOffsetY="0" shapeRotation="0" shapeBlendMode="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeType="0" shapeFillColor="255,255,255,255" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidth="0" shapeBorderWidthUnit="MM" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeOpacity="1"/>
            <shadow shadowOffsetGlobal="1" shadowUnder="0" shadowOffsetUnit="MM" shadowDraw="0" shadowColor="0,0,0,255" shadowBlendMode="6" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOpacity="0.7" shadowOffsetAngle="135" shadowScale="100" shadowRadius="1.5" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetDist="1" shadowRadiusUnit="MM" shadowRadiusAlphaOnly="0"/>
            <substitutions/>
          </text-style>
          <text-format plussign="0" autoWrapLength="0" placeDirectionSymbol="0" formatNumbers="0" useMaxLineLengthForAutoWrap="1" rightDirectionSymbol=">" reverseDirectionSymbol="0" decimals="3" wrapChar="" multilineAlign="3" addDirectionSymbol="0" leftDirectionSymbol="&lt;"/>
          <placement dist="0" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" offsetUnits="MM" distMapUnitScale="3x:0,0,0,0,0,0" rotationAngle="0" maxCurvedCharAngleOut="-25" preserveRotation="1" fitInPolygonOnly="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" centroidInside="0" repeatDistanceUnits="MM" repeatDistance="0" placement="1" placementFlags="10" yOffset="2" xOffset="2" priority="5" distUnits="MM" offsetType="0" quadOffset="8" centroidWhole="0" maxCurvedCharAngleIn="25" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0"/>
          <rendering minFeatureSize="0" scaleMin="0" scaleVisibility="1" limitNumLabels="0" displayAll="0" fontMaxPixelSize="10000" maxNumLabels="2000" fontLimitPixelSize="0" fontMinPixelSize="3" labelPerPart="0" obstacle="1" drawLabels="1" upsidedownLabels="0" scaleMax="1500" zIndex="0" obstacleFactor="1" obstacleType="0" mergeLines="0"/>
          <dd_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </dd_properties>
        </settings>
      </rule>
      <rule filter=" &quot;azimuthDegre&quot; &lt; 0" description="Retour Azimuth négatif " key="{68ba1595-6f46-4d56-ac35-0c8ce7dd8daf}">
        <settings>
          <text-style multilineHeight="1" namedStyle="Regular" fontSize="8" fontWeight="50" fieldName=" round(  &quot;azimuthDegre&quot; ,1)" fontUnderline="0" fontSizeUnit="Pixel" fontStrikeout="0" fontCapitals="0" fontLetterSpacing="0" textColor="0,0,0,255" textOpacity="1" isExpression="1" useSubstitutions="0" fontWordSpacing="0" previewBkgrdColor="#ffffff" fontItalic="0" blendMode="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontFamily="Ubuntu">
            <text-buffer bufferOpacity="1" bufferBlendMode="0" bufferSize="1" bufferDraw="1" bufferSizeUnits="MM" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferJoinStyle="128" bufferColor="253,171,5,255" bufferNoFill="1"/>
            <background shapeSizeX="0" shapeSizeY="0" shapeSizeUnit="MM" shapeSizeType="0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiX="0" shapeBorderColor="128,128,128,255" shapeRadiiY="0" shapeSVGFile="" shapeDraw="0" shapeJoinStyle="64" shapeRotationType="0" shapeOffsetUnit="MM" shapeOffsetX="0" shapeRadiiUnit="MM" shapeOffsetY="0" shapeRotation="0" shapeBlendMode="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeType="0" shapeFillColor="255,255,255,255" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidth="0" shapeBorderWidthUnit="MM" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeOpacity="1"/>
            <shadow shadowOffsetGlobal="1" shadowUnder="0" shadowOffsetUnit="MM" shadowDraw="0" shadowColor="0,0,0,255" shadowBlendMode="6" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOpacity="0.7" shadowOffsetAngle="135" shadowScale="100" shadowRadius="1.5" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetDist="1" shadowRadiusUnit="MM" shadowRadiusAlphaOnly="0"/>
            <substitutions/>
          </text-style>
          <text-format plussign="0" autoWrapLength="0" placeDirectionSymbol="0" formatNumbers="0" useMaxLineLengthForAutoWrap="1" rightDirectionSymbol=">" reverseDirectionSymbol="0" decimals="3" wrapChar="" multilineAlign="3" addDirectionSymbol="0" leftDirectionSymbol="&lt;"/>
          <placement dist="0" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" offsetUnits="MM" distMapUnitScale="3x:0,0,0,0,0,0" rotationAngle="0" maxCurvedCharAngleOut="-25" preserveRotation="1" fitInPolygonOnly="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" centroidInside="0" repeatDistanceUnits="MM" repeatDistance="0" placement="0" placementFlags="10" yOffset="0" xOffset="0" priority="5" distUnits="MM" offsetType="0" quadOffset="4" centroidWhole="0" maxCurvedCharAngleIn="25" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0"/>
          <rendering minFeatureSize="0" scaleMin="0" scaleVisibility="1" limitNumLabels="0" displayAll="0" fontMaxPixelSize="10000" maxNumLabels="2000" fontLimitPixelSize="0" fontMinPixelSize="3" labelPerPart="0" obstacle="1" drawLabels="1" upsidedownLabels="0" scaleMax="750" zIndex="0" obstacleFactor="1" obstacleType="0" mergeLines="0"/>
          <dd_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </dd_properties>
        </settings>
      </rule>
      <rule filter="ELSE" description="Aller " key="{ec93f7f1-ff30-4925-a8c6-be5e9cfffde4}">
        <settings>
          <text-style multilineHeight="1" namedStyle="Regular" fontSize="8" fontWeight="50" fieldName=" round(   &quot;azimuthDegre&quot; ,1)" fontUnderline="0" fontSizeUnit="Pixel" fontStrikeout="0" fontCapitals="0" fontLetterSpacing="0" textColor="0,0,0,255" textOpacity="1" isExpression="1" useSubstitutions="0" fontWordSpacing="0" previewBkgrdColor="#ffffff" fontItalic="0" blendMode="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontFamily="Ubuntu">
            <text-buffer bufferOpacity="0.449" bufferBlendMode="0" bufferSize="1" bufferDraw="1" bufferSizeUnits="MM" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferJoinStyle="128" bufferColor="40,164,88,255" bufferNoFill="1"/>
            <background shapeSizeX="0" shapeSizeY="0" shapeSizeUnit="MM" shapeSizeType="0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiX="0" shapeBorderColor="128,128,128,255" shapeRadiiY="0" shapeSVGFile="" shapeDraw="0" shapeJoinStyle="64" shapeRotationType="0" shapeOffsetUnit="MM" shapeOffsetX="0" shapeRadiiUnit="MM" shapeOffsetY="0" shapeRotation="0" shapeBlendMode="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeType="0" shapeFillColor="255,255,255,255" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidth="0" shapeBorderWidthUnit="MM" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeOpacity="1"/>
            <shadow shadowOffsetGlobal="1" shadowUnder="0" shadowOffsetUnit="MM" shadowDraw="0" shadowColor="0,0,0,255" shadowBlendMode="6" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOpacity="0.7" shadowOffsetAngle="135" shadowScale="100" shadowRadius="1.5" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetDist="1" shadowRadiusUnit="MM" shadowRadiusAlphaOnly="0"/>
            <substitutions/>
          </text-style>
          <text-format plussign="0" autoWrapLength="0" placeDirectionSymbol="0" formatNumbers="0" useMaxLineLengthForAutoWrap="1" rightDirectionSymbol=">" reverseDirectionSymbol="0" decimals="3" wrapChar="" multilineAlign="3" addDirectionSymbol="0" leftDirectionSymbol="&lt;"/>
          <placement dist="0" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" offsetUnits="MM" distMapUnitScale="3x:0,0,0,0,0,0" rotationAngle="0" maxCurvedCharAngleOut="-25" preserveRotation="1" fitInPolygonOnly="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" centroidInside="0" repeatDistanceUnits="MM" repeatDistance="0" placement="0" placementFlags="10" yOffset="0" xOffset="0" priority="5" distUnits="MM" offsetType="0" quadOffset="4" centroidWhole="0" maxCurvedCharAngleIn="25" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0"/>
          <rendering minFeatureSize="0" scaleMin="0" scaleVisibility="1" limitNumLabels="0" displayAll="0" fontMaxPixelSize="10000" maxNumLabels="2000" fontLimitPixelSize="0" fontMinPixelSize="3" labelPerPart="0" obstacle="1" drawLabels="1" upsidedownLabels="0" scaleMax="750" zIndex="0" obstacleFactor="1" obstacleType="0" mergeLines="0"/>
          <dd_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </dd_properties>
        </settings>
      </rule>
    </rules>
  </labeling>
  <customproperties>
    <property key="dualview/previewExpressions">
      <value>jourHeure</value>
    </property>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory backgroundAlpha="255" enabled="0" sizeScale="3x:0,0,0,0,0,0" minScaleDenominator="0" height="15" maxScaleDenominator="1e+8" width="15" labelPlacementMethod="XHeight" rotationOffset="270" diagramOrientation="Up" penWidth="0" opacity="1" lineSizeType="MM" penColor="#000000" scaleBasedVisibility="0" penAlpha="255" scaleDependency="Area" barWidth="5" minimumSize="0" lineSizeScale="3x:0,0,0,0,0,0" sizeType="MM" backgroundColor="#ffffff">
      <fontProperties description="Ubuntu,11,-1,5,50,0,0,0,0,0" style=""/>
      <attribute label="" field="" color="#000000"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings linePlacementFlags="18" dist="0" priority="0" zIndex="0" obstacle="0" placement="0" showAll="1">
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
    <field name="drms">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="fid">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="hauteur">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="hrms">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="jourHeure">
      <editWidget type="DateTime">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="latitude">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="longitude">
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
    <field name="orientation">
      <editWidget type="Range">
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
    <field name="azimuthRadian">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" field="drms" index="0"/>
    <alias name="" field="fid" index="1"/>
    <alias name="" field="hauteur" index="2"/>
    <alias name="" field="hrms" index="3"/>
    <alias name="" field="jourHeure" index="4"/>
    <alias name="" field="latitude" index="5"/>
    <alias name="" field="longitude" index="6"/>
    <alias name="" field="nom" index="7"/>
    <alias name="" field="orientation" index="8"/>
    <alias name="" field="distance" index="9"/>
    <alias name="" field="azimuthDegre" index="10"/>
    <alias name="" field="azimuthRadian" index="11"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="drms" applyOnUpdate="0" expression=""/>
    <default field="fid" applyOnUpdate="0" expression=""/>
    <default field="hauteur" applyOnUpdate="0" expression=""/>
    <default field="hrms" applyOnUpdate="0" expression=""/>
    <default field="jourHeure" applyOnUpdate="0" expression=""/>
    <default field="latitude" applyOnUpdate="0" expression=""/>
    <default field="longitude" applyOnUpdate="0" expression=""/>
    <default field="nom" applyOnUpdate="0" expression=""/>
    <default field="orientation" applyOnUpdate="0" expression=""/>
    <default field="distance" applyOnUpdate="0" expression=""/>
    <default field="azimuthDegre" applyOnUpdate="0" expression=""/>
    <default field="azimuthRadian" applyOnUpdate="0" expression=""/>
  </defaults>
  <constraints>
    <constraint unique_strength="0" field="drms" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="fid" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="hauteur" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="hrms" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="jourHeure" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="latitude" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="longitude" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="nom" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="orientation" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="distance" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="azimuthDegre" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="azimuthRadian" exp_strength="0" constraints="0" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" field="drms" exp=""/>
    <constraint desc="" field="fid" exp=""/>
    <constraint desc="" field="hauteur" exp=""/>
    <constraint desc="" field="hrms" exp=""/>
    <constraint desc="" field="jourHeure" exp=""/>
    <constraint desc="" field="latitude" exp=""/>
    <constraint desc="" field="longitude" exp=""/>
    <constraint desc="" field="nom" exp=""/>
    <constraint desc="" field="orientation" exp=""/>
    <constraint desc="" field="distance" exp=""/>
    <constraint desc="" field="azimuthDegre" exp=""/>
    <constraint desc="" field="azimuthRadian" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortExpression="&quot;jourHeure&quot;" sortOrder="1" actionWidgetStyle="dropDown">
    <columns>
      <column width="214" name="jourHeure" hidden="0" type="field"/>
      <column width="-1" name="drms" hidden="0" type="field"/>
      <column width="-1" name="hrms" hidden="0" type="field"/>
      <column width="-1" name="longitude" hidden="0" type="field"/>
      <column width="-1" name="latitude" hidden="0" type="field"/>
      <column width="-1" name="hauteur" hidden="0" type="field"/>
      <column width="-1" hidden="1" type="actions"/>
      <column width="-1" name="nom" hidden="0" type="field"/>
      <column width="-1" name="fid" hidden="0" type="field"/>
      <column width="-1" name="orientation" hidden="0" type="field"/>
      <column width="-1" name="distance" hidden="0" type="field"/>
      <column width="-1" name="azimuthRadian" hidden="0" type="field"/>
      <column width="-1" name="azimuthDegre" hidden="0" type="field"/>
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
    <field editable="1" name="Azimuth"/>
    <field editable="1" name="Distance"/>
    <field editable="1" name="IdPoint"/>
    <field editable="1" name="azimuth"/>
    <field editable="1" name="azimuthDegre"/>
    <field editable="1" name="azimuthRadian"/>
    <field editable="1" name="distance"/>
    <field editable="1" name="drms"/>
    <field editable="1" name="déviation Est"/>
    <field editable="1" name="déviation Nord"/>
    <field editable="1" name="déviation Z"/>
    <field editable="1" name="fid"/>
    <field editable="1" name="hauteur"/>
    <field editable="1" name="hrms"/>
    <field editable="1" name="jourHeure"/>
    <field editable="1" name="latitude"/>
    <field editable="1" name="longitude"/>
    <field editable="1" name="nom"/>
    <field editable="1" name="ns"/>
    <field editable="1" name="orientatio"/>
    <field editable="1" name="orientation"/>
    <field editable="1" name="précision"/>
  </editable>
  <labelOnTop>
    <field name="Azimuth" labelOnTop="0"/>
    <field name="Distance" labelOnTop="0"/>
    <field name="IdPoint" labelOnTop="0"/>
    <field name="azimuth" labelOnTop="0"/>
    <field name="azimuthDegre" labelOnTop="0"/>
    <field name="azimuthRadian" labelOnTop="0"/>
    <field name="distance" labelOnTop="0"/>
    <field name="drms" labelOnTop="0"/>
    <field name="déviation Est" labelOnTop="0"/>
    <field name="déviation Nord" labelOnTop="0"/>
    <field name="déviation Z" labelOnTop="0"/>
    <field name="fid" labelOnTop="0"/>
    <field name="hauteur" labelOnTop="0"/>
    <field name="hrms" labelOnTop="0"/>
    <field name="jourHeure" labelOnTop="0"/>
    <field name="latitude" labelOnTop="0"/>
    <field name="longitude" labelOnTop="0"/>
    <field name="nom" labelOnTop="0"/>
    <field name="ns" labelOnTop="0"/>
    <field name="orientatio" labelOnTop="0"/>
    <field name="orientation" labelOnTop="0"/>
    <field name="précision" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>jourHeure</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
