#include "sv/sv_interface.h"
#include <stdio.h>
#include <stdlib.h>

int _file_length(FILE *f)
{
	long len;
	fseek(f, 0, SEEK_END);
	len = ftell(f);
	fseek(f, 0, SEEK_SET);
	return len;
}

char* _file_read_buf(char* fn, long *n)
{
	FILE* file = fopen(fn, "rb");
	char* p = 0;
	long len;

	if (file)
	{
		len=file_length(file);
		p = (char*) malloc(len + 1);
		len = fread(p, 1, len, file);
		if (n)
			*n = len;
		fclose(file);
		p[len] = 0;
	}
	return p;
}

/*
Response:
0:success
1:newSVEngine error
2:speaker adapt model failed
*/
int SVtrain(char * sv_cfg_fn , char * sv_output_engine , char * wav_train)
{
	char * data;
	long len;
	int ret=0;
	
	SVEngine *adapt = 0;
	adapt = newSVEngineAdapt(sv_cfg_fn , sv_output_engine , 0);
	if(adapt == NULL)
		return 1;
	// train engine
	data = _file_read_buf(wav_train , &len);
	ret = writeAudioToSVEngineAdaptPass1(adapt , data + 44 , len - 44);
	free(data);

	// generate model
	ret = writeAudioToSVEngineAdaptPass2(adapt);
	if(ret != 0)
		return 2;
	releaseSVEngineAdapt(adapt);
	return 0;
}


/*
Response:
0:success
1:newSVEngine error
2:speaker adapt model failed
*/
int SVtrain3(char * sv_cfg_fn , char * sv_output_engine , char * wav_train1 , char * wav_train2 , char * wav_train3)
{
	char * data;
	long len;
	int ret=0;
	
	SVEngine *adapt = 0;
	adapt = newSVEngineAdapt(sv_cfg_fn , sv_output_engine , 0);
	if(adapt == NULL)
		return 1;

	// train engine
	data = _file_read_buf(wav_train1 , &len);
	ret = writeAudioToSVEngineAdaptPass1(adapt , data + 44 , len - 44);
	free(data);

	// train engine
	data = _file_read_buf(wav_train2 , &len);
	ret = writeAudioToSVEngineAdaptPass1(adapt , data + 44 , len - 44);
	free(data);

	// train engine
	data = _file_read_buf(wav_train3 , &len);
	ret = writeAudioToSVEngineAdaptPass1(adapt , data + 44 , len - 44);
	free(data);

	// generate model
	ret = writeAudioToSVEngineAdaptPass2(adapt);
	if(ret != 0)
		return 2;
	
	releaseSVEngineAdapt(adapt);
	return 0;
}

/*
Response:
0:verify failed;
other: return the index of voice resource
*/
int SVdetect(char * sv_cfg_fn , char * sv_output_engine , char *wav_detect , double thresh , int res_num)
{
	double conf=0.0;
	char *data;
	long len;
	
	SVEngine *detect = 0;
	detect = newSVEngineDetect(sv_cfg_fn , &sv_output_engine , res_num);

	data = _file_read_buf(wav_detect , &len);
	conf = writeAudioToSVEngineDetect2(detect , data + 44 , len - 44 , thresh);

	// printf("conf:%lf\n",conf);
	free(data);
	
	releaseSVEngineDetect(detect);
	return conf;
}
char* test(char *str , double d , int n)    
{    
    puts(str);
    printf("The double is :%f\n", d);
    printf("The int is :%d\n", n); 
    return str;    
}


/*int main()
{
	int ret;
	ret = SVtrain("sv.0.0.3.2.bin" , "test.bin" , "test.wav");
	printf("%d\n", ret);
	ret = SVdetect("sv.0.0.3.2.bin" , "test.bin", "test.wav" , 1.5 , 1);
	printf("%d\n", ret);
	return 0;
}*/
