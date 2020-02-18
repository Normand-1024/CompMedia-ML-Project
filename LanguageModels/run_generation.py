import sys
import gpt_2_simple as gpt2

if len(sys.argv) <= 1:
    exit("Need prompt")

prompt = sys.argv[1]

sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess)

gpt2.generate_to_file(sess,
                            run_name='run1',
                            length=500,
                            temperature=0.7,
                            nsamples=5,
                            prefix=prompt)