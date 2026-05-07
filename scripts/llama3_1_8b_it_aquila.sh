model_str=llama3_1_8b_it_aquila

llamafactory-cli train \
    --stage sft \
    --do_train \
    --template llama3 \
    --model_name_or_path /workspace/MKDS/huggingface/Meta-Llama-3.1-8B-Instruct \
    --learning_rate 1e-4 \
    --dataset aquilamedrt,CMB,medmcqa,medqa \
    --dataset_dir /workspace/MKDS/data \
    --finetuning_type lora \
    --output_dir ${work_dir}/outs/${model_str} \
    --overwrite_cache True \
    --cutoff_len 1024 \
    --warmup_ratio 0.1 \
    --overwrite_output_dir \
    --per_device_train_batch_size 8 \
    --gradient_accumulation_steps 1 \
    --lr_scheduler_type cosine \
    --logging_steps 10 \
    --per_device_eval_batch_size 1 \
    --save_strategy epoch \
    --num_train_epochs 1.0 \
    --plot_loss \
    --fp16 |& tee ${work_dir}/logs/${model_str}.log
