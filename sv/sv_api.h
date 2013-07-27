#ifndef SV_INTERFACE_H_
#define SV_INTERFACE_H_

int SVtrain3(char * sv_cfg_fn , char * sv_output_engine , char * wav_train1 , char * wav_train2 , char * wav_train3);
int SVtrain(char * sv_cfg_fn , char * sv_output_engine , char * wav_train);
int SVdetect(char * sv_cfg_fn , char * sv_output_engine , char *wav_detect, double thresh, int res_num);

#endif	/* SV_INTERFACE_H_ */