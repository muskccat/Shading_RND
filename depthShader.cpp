// Shading RND 
// by Musky
//
// 2016.08.04

#include <maya/MPxNode.h>
#include <maya/MIOStream.h>
#include <maya/MString.h>
#include <maya/MTypeId.h>
#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnLightDataAttribute.h>
#include <maya/MFloatVector.h>
#include <maya/MFnPlugin.h>
#include <maya/MDrawRegistry.h>
#include <maya/MPxSurfaceShadingNodeOverride.h>
#include <maya/MViewPort2Renderer.h>
#include <maya/MFragmentManager.h>


/// Class Declaration
class depthShader : public MPxNode
{
public:
							depthShader();
	virtual			  	 	~depthShader();

	virtual 	Mstatus		compute( const MPlug&, MDataBlock& );
	virtual 	void		postConstructor();

	static	 	void *		creator();
	static 		Mstatus		initialize();

	// ID tag for use with binary file format
	static 		MTypeId 	id;

private:
	//Input attributes
	static	MObject		aColorNear;
	static 	MObject		aColorFar;
	static 	MObject		aNear;
	static 	MObject		aFar;
	static	MObject		aPointCamera;

	//Output attributes
	static	MObject		aOutColor;
};

/// Plug-in Depth shader override declaration

class depthShaderOverride : public MHWRender::MPxSurfaceShadingNodeOverride
{
public:
	static 		MHWRender::MPxSurfaceShadingNodeOverride* creator(const MObject& obj);

	virtual		~depthShaderOverride();

	virtual		MHWRender::DrawAPI supportDrawAPIs()	const;

	virtual 	MString	fragmentName() 					const;

private:
	depthShaderOverride(const MOBject& obj);

	MString		fFragmentName;
};

// Plug-in Depth shader class implementation

// static data
MTypeId depthShader::id( 0x81002 );

// Attributes
MObject depthShader::aColorNear;
MObject depthShader::aColorFar;
MObject depthShader::aNear;
MObject depthShader::aFar;
MObject depthShader::aPointCamera;

MObject depthShader::aOutColor;

#define MAKE_INPUT(attr)		\
	CHECK_MSTATUS(attr.setKeyable(true));		\
	CHECK_MSTATUS(attr.setStroable(true));		\
	CHECK_MSTATUS(attr.setReadable(true));		\
	CHECK_MSTATUS(attr.setWritable(true));		\

#define MAKE_OUTPUT(attr)		\
	CHECK_MSTATUS(attr.setKeyable(false));		\
	CHECK_MSTATUS(attr.setStroable(false));		\
	CHECK_MSTATUS(attr.setReadable(true));		\
	CHECK_MSTATUS(attr.setWritable(false));

void depthShader::postConstructor()
{
	setMPSafe(true);
}

depthShader::depthShader()
{
}

depthShader::~depthShader()
{
}

void* depthSahder::creator()
{
	return new depthShader();
}

Mstatus depthShader::initialize()
{
	MFnNumericAttribute nAttr;

	// Create input attributes

	aColorNear = nAttr.createColor("color",c);
	MAKE_INPUT(nAttr);
	CHECK_MSTATUS(nAttr.setDefault(0., 1., 0.));		//Green

	aColorFar = nAttr.createColor("colorFar","cf");
	MAKE_INPUT(nAttr);
	CHECK_MSTATUS(nAttr.setDefault(0., 0., 1.));		//Blue

	aNear = nAttr.create("near", "n", MFnNumericData::kFloat);
	MAKE_INPUT(nAttr);
	CHECK_MSTATUS(nAttr.setMin(0.0f));
	CHECK_MSTATUS(nAttr.setSoftMax(1000.0f));
	
	aFar = nAttr.create("far","f", MFnNumericData::kFloat);
	MAKE_INPUT(nAttr);
	CHECK_MSTATUS(nAttr.setMin(0.0f));
	CHECK_MSTATUS(nAttr.setSoftMax(1000.0f));
	CHECK_MSTATUS(nAttr.setDefault(2.0f));

	aPointCamera = nAttr.createPoint("pointCamera", "p");
	MAKE_INPUT(nAttr);
	CHECK_MSTATUS(nAttr.setHidden(true));

	// Create output attributes
	aOutColor = nAttr.createColor("outColor", "oc");
	MAKE_OUTPUT(nAttr);

	CHECK_MSTATUS(addAttribute(aColorNear));
	CHECK_MSTATUS(addAttribute(aColorFar));
	CHECK_MSTATUS(addAttribute(aNear));
	CHECK_MSTATUS(addAttribute(aFar));
	CHECK_MSTATUS(addAttribute(aPointCamera));
	CHECK_MSTATUS(addAttribute(aOutColor));

	CHECK_MSTATUS(attributeAffects(aColorNear, aOutColor));
	CHECK_MSTATUS(attributeAffects(aColorFar, aOutColor));
	CHECK_MSTATUS(attributeAffects(aNear, 	aOutColor));
	CHECK_MSTATUS(attributeAffects(aFar, aOutColor));
	CHECK_MSTATUS(attributeAffects(aPointCamera, aOutColor));

	return MS::kSuccess;
}

MStatus depthShader::compute(const MPlug& 	plug, MDataBlock& block)
{
	//Outcolor or individual R,G,B Channel
	if ((plug != aOutColor) && (plug.parent() != aOutColor))
			return MS::kUnknownParameter;

	MFloatVector resultColor;

	// get sample surface shading parametes
	MFloatVector& pCamera 	= block.inputValue(aPointCamera).asFloatVector();
	MFloatVector& cNear 	= block.inputValue(aColorNear).asFloatVector();
	MFloatVector& cFar 		= block.inputValue(aColorFar).asFloatVector();
	float nearClip			= block.inputValue(aNear).asFloat();
	float farClip			= block.inputValue(aFar).asFloat();

	// pCamera.z is negative
	float ratio = (farClip + pCamera.z) / ( farClip - nearClip );
	resultColor = cNear * ratio + cFar*(1.f - ratio);

	// set output color attribute
	MDataHandle outColorHandle = block.outputValue( aOutColor );
	MFloatVector& outColor = outColorHandle.asFloatVector();
	outColor = resultColor;
	outColorHandle.setClean();

	return MS::kSuccess;
}

