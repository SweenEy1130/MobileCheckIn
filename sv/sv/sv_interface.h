/*
 * sv_interface.h
 *
 *  Created on: Aug 22, 2012
 *      Author: fx310
 */

#ifndef SV_INTERFACE_H_
#define SV_INTERFACE_H_

#ifdef __cplusplus
extern "C" {
#endif

typedef struct SV SVEngine;

SVEngine* newSVEngineAdapt(char* resBinFile, char* spkrModelFile, char* context);
int writeAudioToSVEngineAdaptPass1(SVEngine* engine, char* audio, int bytesLen);
int writeAudioToSVEngineAdaptPass2(SVEngine* engine);
void releaseSVEngineAdapt(SVEngine* engine);

SVEngine* newSVEngineDetect(char* resBinFile, char** spkrModelFile, int spkrModelNum);
int writeAudioToSVEngineDetect(SVEngine* engine, char* audio, int bytesLen, double threshold);
void releaseSVEngineDetect(SVEngine* engine);

#ifdef __cplusplus
};
#endif

#endif	/* SV_INTERFACE_H_ */
