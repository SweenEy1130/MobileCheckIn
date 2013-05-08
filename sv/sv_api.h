#ifndef SV_INTERFACE_H_
#define SV_INTERFACE_H_

int SVtrain(char * sv_cfg_fn , char * sv_output_engine , char * wav_train);
int SVdetect(char * sv_cfg_fn , char * sv_output_engine , char *wav_detect, double thresh, int res_num);
char* test(char *str , double d , int n);

#endif	/* SV_INTERFACE_H_ */