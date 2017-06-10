python prepare_data_one_vs_rest.py ../train_stack_overflow.txt ../onevsrest_data/
python3.4 nb_one_vs_rest.py ../test.txt ../onevsrest_data/ ../nb_output/
python3.4 svm_one_vs_rest.py ../test.txt ../onevsrest_data/ ../svm_output/

