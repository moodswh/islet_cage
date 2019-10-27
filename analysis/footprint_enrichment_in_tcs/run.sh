workflow="footprint_enrichment_in_tcs"
snakedir="$BASE_DIR/analysis/${workflow}"
configdir="${snakedir}/configs"
scriptdir="${snakedir}/scripts"
logdir="$BASE_DIR/work/${workflow}/logs"
datadir="$BASE_DIR/work/${workflow}/data"
mkdir -p $datadir
mkdir -p $logdir

# make config
python ${scriptdir}/mkconfig.py --base ${BASE_DIR} --email ${email} --config ${configdir}/config.yaml --workflow ${workflow}

# # print workflow
snakemake -nprs ${scriptdir}/Snakefile_GAT --rulegraph --configfile ${configdir}/config.yaml | dot -Tsvg > ${configdir}/${workflow}.svg

# Submit jobs
snakemake --cluster-config ${configdir}/cluster.yaml \
		  --cluster "sbatch --time {cluster.time} --mem {cluster.mem} --cpus-per-task {cluster.cpus} --job-name {cluster.jobname} -o {cluster.output} -e {cluster.error}  --parsable "  \
		  -j 60 --latency-wait 400 -prs ${scriptdir}/Snakefile_GAT --configfile ${configdir}/config.yaml $1


