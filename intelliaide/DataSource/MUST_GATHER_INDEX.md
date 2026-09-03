---
# Must-Gather Directory and File Index

Quick reference index for LLM routing. Use this for fast lookups of directories and files by problem keywords.

## Directory Structure Quick Index

User supplies **`<must-gather-root>`**. Under it there is **one folder `<content-folder>`** (any name, e.g. `quay-content`). Under that folder:

```
<must-gather-root>/
└── <content-folder>/                              # one child, any name (e.g. quay-content)
    ├── version                                    # Must-gather version info
    ├── event-filter.html                          # ★ All events in searchable web UI
    │
    ├── ── CLUSTER-WIDE RESOURCES ──
    ├── cluster-scoped-resources/                   # All cluster-level objects
    │   ├── config.openshift.io/                    # ★ PRIMARY: Cluster configuration
    │   │   ├── clusteroperators.yaml               #   ★ START HERE: Operator health
    │   │   ├── clusterversions.yaml                #   Version, upgrade status, history
    │   │   ├── infrastructures/                    #   Platform (AWS/Azure/GCP/bare-metal)
    │   │   ├── networks.yaml                       #   CNI type, pod/service CIDRs
    │   │   ├── dnses.yaml                          #   DNS upstream servers, cluster domain
    │   │   ├── proxies.yaml                        #   HTTP/HTTPS proxy config
    │   │   ├── apiservers.yaml                     #   API server config, audit
    │   │   ├── schedulers.yaml                     #   Scheduler policies
    │   │   ├── authentications/                    #   OAuth providers, token config
    │   │   ├── featuregates/                       #   Enabled features
    │   │   ├── images.yaml                         #   Image config, registry sources
    │   │   ├── consoles/                           #   Web console config
    │   │   ├── nodes.yaml                          #   Node configuration
    │   │   └── oauths.yaml                         #   OAuth configuration
    │   │
    │   ├── core/                                   # Kubernetes core resources
    │   │   ├── nodes/                              #   ★ Per-node YAML (status, taints, labels)
    │   │   │   └── <node-name>.yaml
    │   │   ├── namespaces.yaml                     #   All namespace definitions
    │   │   └── persistentvolumes/                  #   Cluster-wide PVs
    │   │       └── <pv-name>.yaml
    │   │
    │   ├── machineconfiguration.openshift.io/      # Node OS & config
    │   │   ├── machineconfigs/                     #   OS configs (compare rendered-* for changes)
    │   │   ├── machineconfigpools/                 #   Pools (master/worker) update status
    │   │   ├── machineconfignodes/                 #   Per-node config state
    │   │   ├── kubeletconfigs/                     #   ★ KubeletConfig (autoSizingReserved, systemReserved)
    │   │   └── controllerconfigs/                  #   MCO settings
    │   │
    │   ├── rbac.authorization.k8s.io/              # RBAC (authorization issues)
    │   │   ├── clusterroles.yaml
    │   │   └── clusterrolebindings.yaml
    │   │
    │   ├── storage.k8s.io/                         # Storage
    │   │   ├── storageclasses.yaml
    │   │   ├── csinodes.yaml                       #   CSI driver registration per node
    │   │   ├── csidrivers.yaml
    │   │   └── volumeattachments/                  #   Volume→node attachments
    │   │       └── <attachment-name>.yaml
    │   │
    │   ├── apiregistration.k8s.io/                 # API services (APIService availability)
    │   │   └── apiservices/
    │   ├── admissionregistration.k8s.io/           # Webhooks (validation/mutation)
    │   ├── apiextensions.k8s.io/                   # CRDs (custom resource definitions)
    │   │   └── customresourcedefinitions/
    │   ├── security.openshift.io/                  # SCCs (pod security)
    │   │   └── securitycontextconstraints.yaml
    │   ├── oauth.openshift.io/                     # OAuth clients
    │   ├── operators.coreos.com/                   # OLM (installed operators)
    │   ├── operator.openshift.io/                  # Operator configs
    │   └── snapshot.storage.k8s.io/                # Volume snapshots
    │
    ├── ── NAMESPACE RESOURCES ──
    ├── namespaces/<namespace>/                     # Per-namespace data
    │   ├── <namespace>.yaml                        #   Namespace definition
    │   ├── core/                                   #   Core K8s resources
    │   │   ├── events.yaml                         #   ★ CRITICAL: All events (errors, warnings)
    │   │   ├── pods.yaml                           #   All pod definitions & status (aggregated)
    │   │   ├── configmaps.yaml                     #   ConfigMap data
    │   │   ├── secrets.yaml                        #   Secret names (values redacted)
    │   │   ├── services.yaml                       #   Service definitions
    │   │   ├── endpoints.yaml                      #   Service endpoints (backend pods)
    │   │   ├── persistentvolumeclaims.yaml         #   PVCs, binding status
    │   │   ├── replicationcontrollers.yaml         #   Replication controllers
    │   │   ├── serviceaccounts.yaml                #   Service accounts
    │   │   └── resourcequotas.yaml                 #   Resource quotas
    │   │
    │   ├── apps/                                   #   Application workloads
    │   │   ├── deployments.yaml                    #   Deployments, replica status
    │   │   ├── daemonsets.yaml                     #   DaemonSets, scheduled nodes
    │   │   ├── statefulsets.yaml                   #   StatefulSets, persistent state
    │   │   └── replicasets.yaml                    #   ReplicaSets (owned by Deployments)
    │   │
    │   ├── batch/                                  #   Jobs & CronJobs
    │   │   ├── jobs.yaml                           #   Job status, completion
    │   │   └── cronjobs.yaml                       #   Scheduled jobs
    │   │
    │   ├── autoscaling/                            #   Autoscaling
    │   │   └── horizontalpodautoscalers.yaml       #   HPA rules, current replicas
    │   │
    │   ├── networking.k8s.io/                      #   Network policies
    │   │   ├── networkpolicies.yaml                #   Ingress/egress rules
    │   │   └── ingresses.yaml                      #   Ingress resources
    │   │
    │   ├── route.openshift.io/                     #   OpenShift routes
    │   │   └── routes.yaml                         #   HTTP/HTTPS routes
    │   │
    │   ├── monitoring.coreos.com/                  #   Monitoring (if enabled)
    │   │   ├── servicemonitors.yaml                #   Prometheus scrape configs
    │   │   └── prometheusrules.yaml                #   Alerting rules
    │   │
    │   ├── policy/                                 #   Pod policies
    │   │   └── poddisruptionbudgets.yaml           #   PDB (disruption limits)
    │   │
    │   ├── rbac.authorization.k8s.io/              #   Namespace-scoped RBAC
    │   │   ├── roles.yaml
    │   │   └── rolebindings.yaml
    │   │
    │   └── pods/<pod-name>/                        #   ★ Per-pod detailed data
    │       ├── <pod-name>.yaml                     #   Pod spec, status, conditions
    │       └── <container-name>/                   #   Per-container data
    │           └── <container-name>/
    │               └── logs/
    │                   ├── current.log             #   ★ Active container logs
    │                   ├── previous.log            #   ★ Crashed container logs
    │                   └── previous.insecure.log   #   Previous logs (unfiltered)
    │
    ├── ── CRITICAL NAMESPACES (Platform Components) ──
    │   │
    │   │   ── Control Plane ──
    │   ├── openshift-kube-apiserver/               # Kubernetes API server
    │   ├── openshift-kube-controller-manager/      # K8s controllers
    │   ├── openshift-kube-scheduler/               # Pod scheduler
    │   ├── openshift-etcd/                         # Etcd datastore
    │   │
    │   │   ── OpenShift API ──
    │   ├── openshift-apiserver/                    # OpenShift API extensions
    │   ├── openshift-controller-manager/           # OpenShift controllers
    │   ├── openshift-oauth-apiserver/              # OAuth API
    │   ├── openshift-authentication/               # OAuth server (login)
    │   │
    │   │   ── Cluster Lifecycle ──
    │   ├── openshift-cluster-version/              # Cluster upgrades (CVO)
    │   ├── openshift-machine-config-operator/      # Node config/OS updates
    │   ├── openshift-machine-api/                  # Machine lifecycle
    │   │
    │   │   ── Networking ──
    │   ├── openshift-ovn-kubernetes/               # Networking (OVN CNI)
    │   ├── openshift-dns/                          # CoreDNS
    │   ├── openshift-multus/                       # Multi-network
    │   ├── openshift-network-operator/             # Network operator
    │   │
    │   │   ── Ingress ──
    │   ├── openshift-ingress/                      # HAProxy routers
    │   ├── openshift-ingress-operator/             # Ingress operator
    │   │
    │   │   ── Platform Services ──
    │   ├── openshift-image-registry/               # Internal registry
    │   ├── openshift-monitoring/                   # Prometheus stack
    │   ├── openshift-console/                      # Web console
    │   │
    │   │   ── Storage ──
    │   ├── openshift-cluster-storage-operator/     # Storage operator
    │   ├── openshift-cluster-csi-drivers/          # CSI drivers
    │   │
    │   │   ── Other Operators ──
    │   ├── openshift-cluster-node-tuning-operator/ # Node performance
    │   ├── openshift-operator-lifecycle-manager/   # OLM
    │   ├── openshift-marketplace/                  # OperatorHub
    │   ├── openshift-config/                       # Cluster config storage
    │   ├── openshift-config-managed/               # System-managed configs
    │   ├── openshift-service-ca/                   # Service cert CA
    │   └── openshift-insights/                     # Red Hat Insights
    │
    ├── ── NODE DIAGNOSTICS ──
    ├── nodes/<node-name>/                          # Per-node system data (use nodes/<node-name>/* to fetch all — bare dir does not resolve)
    │   ├── <node-name>_logs_kubelet.gz             # ★ Kubelet logs (compressed)
    │   ├── dmesg                                   # Kernel messages (OOM, hardware faults)
    │   ├── sysinfo.log                             # System info (df, ps, uptime)
    │   ├── proc_cmdline                            # Kernel boot parameters
    │   ├── lscpu                                   # CPU topology
    │   ├── lspci                                   # PCI devices
    │   ├── ethtool_channels                        # NIC queue/channel config
    │   ├── ethtool_features                        # NIC offload/feature flags
    │   ├── cpu_affinities.json                     # CPU affinity / NUMA data
    │   ├── irq_affinities.json                     # IRQ-to-CPU affinity mapping
    │   ├── podresources.json                       # Pod resource allocation
    │   ├── pods_info.json                          # Pods on node
    │   └── sysinfo.tgz                             # Full system diagnostic archive
    │
    ├── host_service_logs/                          # ★ Systemd service logs
    │   ├── masters/                                #   Master node services
    │   │   ├── kubelet_service.log                 #   ★ Kubelet (pod management)
    │   │   ├── crio_service.log                    #   ★ CRI-O container runtime
    │   │   ├── machine-config-daemon-firstboot_service.log  # MCO first boot
    │   │   ├── machine-config-daemon-host_service.log       # MCO host service
    │   │   ├── openvswitch_service.log             #   OVS (network dataplane)
    │   │   ├── NetworkManager_service.log          #   Network interface config
    │   │   ├── ovs-configuration_service.log       #   OVS configuration
    │   │   ├── ovs-vswitchd_service.log            #   OVS daemon
    │   │   ├── ovsdb-server_service.log            #   OVS database server
    │   │   ├── rpm-ostreed_service.log             #   OS updates (rpm-ostree)
    │   │   └── ostree-finalize-staged_service.log  #   OS staging
    │   ├── workers/                                #   Worker node services (same structure)
    │   └── windows/                                #   Windows node logs (conditional)
    │       └── log_files/
    │           ├── kubelet/kubelet.log
    │           ├── kube-proxy/kube-proxy.log
    │           ├── containerd/containerd.log
    │           ├── hybrid-overlay/hybrid-overlay.log
    │           ├── wicd/
    │           └── csi-proxy/csi-proxy.log
    │
    ├── ── ETCD DIAGNOSTICS ──
    ├── etcd_info/                                  # Etcd cluster health
    │   ├── endpoint_health.json                    # ★ Member health (healthy/unhealthy)
    │   ├── member_list.json                        # Cluster membership, leader
    │   ├── endpoint_status.json                    # DB size, raft index per member
    │   ├── alarm_list.json                         # Active alarms (NOSPACE, CORRUPT)
    │   └── object_count.json                       # Object counts by resource type
    │
    ├── ── NETWORK DIAGNOSTICS ──
    ├── network_logs/                               # Network-specific data
    │   ├── ovnk_database_store.tar.gz              # ★ OVN NB/SB databases (compressed; per-node in interconnect mode)
    │   ├── ovnk_extras_store.tar.gz                # Extra libovsdb logs (interconnect mode ONLY)
    │   ├── ovn_kubernetes_top_pods                  # OVN pod resource usage
    │   ├── cluster_scale                           # Network scale metrics
    │   ├── leader_ovnnb_status                     # OVN Northbound leader status (LEGACY/single-zone mode ONLY)
    │   ├── leader_ovnsb_status                     # OVN Southbound leader status (LEGACY/single-zone mode ONLY)
    │   ├── leader_nbdb                             # Leader NB database file (LEGACY/single-zone mode ONLY)
    │   ├── leader_sbdb                             # Leader SB database file (LEGACY/single-zone mode ONLY)
    │   ├── net-attach-def/                         # NetworkAttachmentDefinitions (multus)
    │   ├── multi-networkpolicy/                    # Multi-network policies
    │   ├── ippools.*.yaml                          # IP pool allocations
    │   └── ipsec/                                  # IPsec data (conditional)
    │       ├── status/
    │       ├── trafficstatus/
    │       ├── xfrm/
    │       ├── <pod-name>_ipsec.conf
    │       └── <pod-name>_libreswan.log
    │
    ├── pod_network_connectivity_check/             # Connectivity test results
    │   └── podnetworkconnectivitychecks.yaml
    │
    ├── ── MONITORING DATA ──
    ├── monitoring/                                 # Prometheus & Alertmanager (conditional)
    │   ├── prometheus/                             #   Prometheus configs, rules, targets
    │   │   ├── alertmanagers.json
    │   │   ├── rules.json
    │   │   ├── status/config.json
    │   │   ├── status/flags.json
    │   │   ├── <pod-name>/active-targets.json
    │   │   ├── <pod-name>/status/runtimeinfo.json
    │   │   └── <pod-name>/status/tsdb.json
    │   ├── alertmanager/                           #   Alertmanager config, silences
    │   │   ├── status.json
    │   │   └── status.stderr
    │   └── metrics/                                #   Metrics dump (conditional)
    │       ├── metrics.openmetrics
    │       └── metrics.stderr
    │
    ├── ── INGRESS / ROUTING ──
    ├── ingress_controllers/                        # Per-ingress-controller data
    │   └── <ingress-controller-name>/
    │       └── <pod-name>/haproxy.config
    │
    ├── ── AUDIT LOGS ──
    ├── audit_logs/                                 # API server audit logs (conditional)
    │   ├── kube-apiserver/                         #   K8s API server audit
    │   │   └── <node-name>-audit.log
    │   ├── openshift-apiserver/                    #   OpenShift API server audit
    │   │   └── <node-name>-audit.log
    │   ├── oauth-apiserver/                        #   OAuth API server audit
    │   │   └── <node-name>-audit.log
    │   ├── oauth-server/                           #   OAuth server audit
    │   │   └── <node-name>-audit.log
    │   ├── etcd/                                   #   etcd audit logs
    │   │   └── <node-name>-audit.log
    │   └── monitoring/                             #   Monitoring audit logs
    │       └── <pod-name>-audit.log
    │
    ├── ── SPECIAL DIAGNOSTICS ──
    ├── machine_config_ondisk/                      # On-disk configs (degraded nodes only)
    │   └── <node-name>/
    │       ├── mcs-machine-config-content.json     #   Applied config from MCS
    │       └── bootstrapconfigdiff                 #   Diff from bootstrap
    │
    ├── machine_config_termination_logs/            # MCD termination logs
    │
    ├── static-pods/                                # Static pod failure logs
    │   └── kube-apiserver/
    │       ├── <node-name>-startup.log.gz          #   API server startup (compressed)
    │       └── <node-name>-termination.log.gz      #   API server termination (compressed)
    │
    ├── insights-data/                              # Red Hat Insights archive
    │   └── insights-<timestamp>.tar.gz
    │
    └── istio/                                      # Service mesh (conditional)
        └── cluster-scoped-resources/
```

---

## Decision Matrix: Problem Type → Primary Files

### 1. Cluster Health / Operator Issues

**Keywords**: `cluster operator`, `operator degraded`, `operator`, `control plane`, `available`, `progressing`, `cluster version`, `upgrade`, `update`

START HERE for any cluster-wide issue:

1. `cluster-scoped-resources/config.openshift.io/clusteroperators.yaml`
   → Shows which operators are Degraded/Progressing/Available
2. `cluster-scoped-resources/config.openshift.io/clusterversions.yaml`
   → Version, upgrade status, history, conditions
3. `namespaces/openshift-<degraded-operator>/core/events.yaml`
   → Why the operator is degraded
4. `namespaces/openshift-<degraded-operator>/pods/*/<container>/<container>/logs/current.log`
   → Operator pod logs

THEN check specific component based on degraded operator.

---

### 2. Pod / Container Issues

**Keywords**: `pod`, `container`, `crash`, `restart`, `pending`, `image pull`, `CrashLoopBackOff`, `ImagePullBackOff`, `OOMKilled`, `evicted`, `probe`, `terminating`

**Pod won't start / crashes / restarts / CrashLoopBackOff / ImagePullBackOff:**

1. `namespaces/<namespace>/core/events.yaml`
   → Error messages, reason (ImagePullBackOff, OOMKilled, etc.)
2. `namespaces/<namespace>/core/pods.yaml`
   → Pod status, conditions, resource requests/limits
3. `namespaces/<namespace>/pods/<pod-name>/<container-name>/<container-name>/logs/current.log`
   → Application logs
4. `namespaces/<namespace>/pods/<pod-name>/<container-name>/<container-name>/logs/previous.log`
   → Logs from crashed container (if pod restarted)
5. `nodes/<node-name>/<node-name>_logs_kubelet.gz`
   → Kubelet perspective (mount failures, runtime errors) (compressed)
6. `host_service_logs/masters|workers/crio_service.log`
   → Container runtime errors (image pull, storage)
7. `host_service_logs/masters|workers/kubelet_service.log`
   → Systemd kubelet logs

**Pod pending / not scheduling:**

1. `namespaces/<namespace>/core/events.yaml` → `FailedScheduling` reason
2. `cluster-scoped-resources/core/nodes/*.yaml` → Check node capacity, taints
3. `namespaces/<namespace>/core/pods.yaml` → nodeSelector, tolerations, affinity

---

### 3. Node Issues

**Keywords**: `node`, `NotReady`, `degraded node`, `high CPU`, `memory`, `disk full`, `OOM`, `reboot`, `machine config`, `kubelet`

**Node NotReady / degraded / high CPU/memory / disk full:**

1. `cluster-scoped-resources/core/nodes/<node-name>.yaml`
   → Node conditions (Ready, MemoryPressure, DiskPressure, PIDPressure)
2. **If masters NotReady / NodeStatusUnknown — check EXTERNAL DNS / API first:**
   - `cluster-scoped-resources/config.openshift.io/infrastructures.yaml`
   - `cluster-scoped-resources/config.openshift.io/dnses.yaml`
   - `pod_network_connectivity_check/podnetworkconnectivitychecks.yaml`
   - `host_service_logs/masters/kubelet_service.log` (lookup / lease / dial to api)
3. `namespaces/<any>/core/events.yaml` (filter by node)
   → Node-related events
4. `nodes/<node-name>/dmesg`
   → Kernel messages (OOM kills, hardware errors, panics)
5. `nodes/<node-name>/sysinfo.log`
   → df, ps, uptime, memory, disk usage
6. `nodes/<node-name>/<node-name>_logs_kubelet.gz`
   → Kubelet issues (pod evictions, PLEG) (compressed)
7. `host_service_logs/masters|workers/kubelet_service.log`
   → Systemd kubelet

**Node reboots / config changes:**

8. `host_service_logs/masters|workers/machine-config-daemon-firstboot_service.log`
9. `host_service_logs/masters|workers/machine-config-daemon-host_service.log`
10. `cluster-scoped-resources/machineconfiguration.openshift.io/machineconfigpools/`
11. `cluster-scoped-resources/machineconfiguration.openshift.io/machineconfigs/`

**Machine not provisioning / not joining:**

12. `namespaces/openshift-machine-api/core/events.yaml`
13. `namespaces/openshift-machine-api/pods/*/logs/current.log` and `previous.log`
14. `cluster-scoped-resources/config.openshift.io/infrastructures.yaml`

---

### 4. Networking Issues

**Keywords**: `network`, `connectivity`, `dns`, `pod network`, `service`, `route`, `ingress`, `ovn`, `multus`, `sdn`, `network policy`, `egress`, `api-int`, `no such host`, `NXDOMAIN`, `external DNS`, `NotReady`

**External / infrastructure DNS (API hostname resolution) — CHECK FIRST for
NotReady masters, API unreachable, control-plane outage:**

1. `cluster-scoped-resources/config.openshift.io/infrastructures.yaml`
   → Required external DNS names (api / api-int / apps)
2. `cluster-scoped-resources/config.openshift.io/dnses.yaml`
   → Cluster domain + upstream external DNS servers
3. `pod_network_connectivity_check/podnetworkconnectivitychecks.yaml`
   → Failed API/DNS connectivity checks
4. `host_service_logs/masters/kubelet_service.log`
   → Lookup / dial failures to API endpoints
5. `host_service_logs/masters/NetworkManager_service.log`
   → Resolver / DHCP client symptoms (secondary unless proven primary)

**Internal DNS (CoreDNS) — pod/service name resolution:**

6. `namespaces/openshift-dns/core/events.yaml`
7. `namespaces/openshift-dns/pods/dns-default-*/<container>/<container>/logs/current.log`

**CNI / OVN (only after DNS/API resolution ruled out or separately implicated):**

8. `cluster-scoped-resources/config.openshift.io/networks.yaml`
   → CNI type, pod CIDR, service CIDR
9. `namespaces/openshift-ovn-kubernetes/pods/ovnkube-node-*/<container>/<container>/logs/current.log`
   → OVN CNI logs (pod network setup)
10. `namespaces/openshift-ovn-kubernetes/pods/ovnkube-control-plane-*/<container>/<container>/logs/current.log`
   → OVN control plane
11. `network_logs/ovnk_database_store.tar.gz`
   → OVN northbound/southbound DB (flow rules) (compressed)
12. `host_service_logs/masters|workers/openvswitch_service.log`
   → OVS dataplane
13. `pod_network_connectivity_check/podnetworkconnectivitychecks.yaml`
   → Network connectivity test results

**Route / Ingress issues:**

14. `namespaces/openshift-ingress/pods/router-*/<container>/<container>/logs/current.log`
15. `ingress_controllers/default/<pod-name>/haproxy.config`
16. `namespaces/<namespace>/route.openshift.io/routes.yaml`

**OVN alerts / readiness:**

- `network_logs/leader_ovnnb_status`, `leader_ovnsb_status`, `ovn_kubernetes_top_pods` — **the two `leader_*` files exist only in legacy/single-zone OVN mode**; in interconnect mode (multi-zone, the current default) use `network_logs/ovnk_database_store.tar.gz` and `network_logs/ovnk_extras_store.tar.gz` instead
- `monitoring/alertmanager/`, `monitoring/prometheus/`

**IPsec:**

- `network_logs/ipsec/trafficstatus/`, `network_logs/ipsec/status/`
- `network_logs/ipsec/<pod-name>_ipsec.conf`, `<pod-name>_libreswan.log`

**NMState / Multus / EgressIP (conditionally collected):**

- NMState: `cluster-scoped-resources/nmstate.io/nodenetworkstates/`, `nodenetworkconfigurationpolicies/`
- Multus: `cluster-scoped-resources/k8s.cni.cncf.io/net-attach-def/`, `ippools/`, `multi-networkpolicy/`
- OVN-K CRs: `cluster-scoped-resources/k8s.ovn.org/egressips/`, `clusteruserdefinednetworks/`
- SDN: `cluster-scoped-resources/network.openshift.io/hostsubnets/`

**SR-IOV / MetalLB / FRR:**

- `namespaces/openshift-sriov-network-operator/`
- `namespaces/openshift-metallb-operator/`
- `namespaces/openshift-frr-k8s/`

---

### 5. Storage Issues

**Keywords**: `storage`, `volume`, `pvc`, `pv`, `persistent volume`, `csi`, `mount`, `attach`, `detach`, `storage class`

**PVC not binding / volume mount failures / attachment errors:**

1. `cluster-scoped-resources/storage.k8s.io/storageclasses.yaml`
   → Available storage classes, provisioner
2. `cluster-scoped-resources/core/persistentvolumes/`
   → PV status (Available/Bound/Released/Failed)
3. `namespaces/<namespace>/core/persistentvolumeclaims.yaml`
   → PVC status, requested vs allocated
4. `namespaces/<namespace>/core/events.yaml`
   → Provisioning failures, mount errors
5. `cluster-scoped-resources/storage.k8s.io/volumeattachments/`
   → Volume attachment to nodes
6. `cluster-scoped-resources/storage.k8s.io/csinodes.yaml`
   → CSI driver availability per node
7. `namespaces/openshift-cluster-csi-drivers/pods/*/<container>/<container>/logs/current.log`
   → CSI driver logs
8. `nodes/<node-name>/<node-name>_logs_kubelet.gz`
   → Volume mount failures (compressed)

---

### 6. Authentication / Authorization

**Keywords**: `login`, `authentication`, `authorization`, `oauth`, `rbac`, `permission denied`, `forbidden`, `401`, `403`, `service account`, `token`

**Login failures / permission denied / RBAC issues:**

1. `cluster-scoped-resources/config.openshift.io/authentications/`
   → Identity providers, OAuth config
2. `cluster-scoped-resources/config.openshift.io/oauths.yaml`
   → OAuth clients/config
3. `cluster-scoped-resources/config.openshift.io/proxies.yaml`
   → When external IdP connectivity may fail
4. `namespaces/openshift-authentication/pods/oauth-openshift-*/<container>/<container>/logs/current.log`
   → OAuth server logs (login attempts)
5. `namespaces/openshift-oauth-apiserver/pods/*/<container>/<container>/logs/current.log`
   → OAuth API server
6. `cluster-scoped-resources/rbac.authorization.k8s.io/`
   → ClusterRoles, ClusterRoleBindings
7. `namespaces/<namespace>/core/serviceaccounts.yaml`
   → Service account definitions
8. `namespaces/openshift-authentication/core/events.yaml`
   → Authentication errors
9. `audit_logs/oauth-apiserver/<node-name>-audit.log` (Conditional)
   → OAuth API audit trail
10. `audit_logs/oauth-server/<node-name>-audit.log` (Conditional)
   → OAuth server audit trail
11. `cluster-scoped-resources/security.openshift.io/securitycontextconstraints.yaml`
   → SCC definitions (pod security)

---

### 7. API Server Issues

**Keywords**: `api server`, `apiserver`, `slow`, `timeout`, `503`, `unavailable`, `throttling`, `api priority`, `fairness`

**API slow / timeouts / 503 errors / unavailable:**

0. `cluster-scoped-resources/config.openshift.io/infrastructures.yaml` + `dnses.yaml`
   → Confirm required API hostnames and upstream DNS (external resolution) BEFORE assuming apiserver process failure
1. `pod_network_connectivity_check/podnetworkconnectivitychecks.yaml`
2. `namespaces/openshift-kube-apiserver/pods/kube-apiserver-*/kube-apiserver/kube-apiserver/logs/current.log`
   → API server request logs, errors
3. `namespaces/openshift-kube-apiserver/pods/kube-apiserver-*/kube-apiserver/kube-apiserver/api_priority_and_fairness/queues`
   → Throttling, request queuing
4. `namespaces/openshift-kube-apiserver/pods/kube-apiserver-*/kube-apiserver/kube-apiserver/api_priority_and_fairness/priority_levels`
   → Priority configuration
5. `namespaces/openshift-kube-apiserver/pods/kube-apiserver-*/kube-apiserver/kube-apiserver/api_priority_and_fairness/requests`
   → Current in-flight requests
6. `cluster-scoped-resources/config.openshift.io/apiservers.yaml`
   → API server configuration
7. `etcd_info/endpoint_health.json`
   → Etcd health (API backend)
8. `etcd_info/alarm_list.json`
   → Etcd alarms (NOSPACE causes API failures)
9. `namespaces/openshift-kube-apiserver/core/events.yaml`
   → API server pod issues
10. `audit_logs/kube-apiserver/<node-name>-audit.log` (Conditional)
   → API request audit trail
11. `static-pods/kube-apiserver/<node-name>-startup.log.gz` (compressed)
12. `static-pods/kube-apiserver/<node-name>-termination.log.gz` (compressed)

---

### 8. Etcd Issues

**Keywords**: `etcd`, `quorum`, `member`, `alarm`, `slow`, `grpc`, `endpoint`, `database`, `corruption`, `etcdGRPCRequestsSlow`, `NOSPACE`, `CORRUPT`

**Quorum loss / slow commits / database size / alarms:**

1. `etcd_info/endpoint_health.json`
   → Member health status
2. `etcd_info/member_list.json`
   → Members, leader, raft status
3. `etcd_info/alarm_list.json`
   → Active alarms (NOSPACE, CORRUPT)
4. `etcd_info/endpoint_status.json`
   → DB size, raft index per member
5. `etcd_info/object_count.json`
   → Object counts (identify bloat)
6. `namespaces/openshift-etcd/pods/etcd-*/etcd/etcd/logs/current.log`
   → Etcd logs (leader elections, compaction)
7. `namespaces/openshift-etcd/core/events.yaml`
   → Etcd pod issues
8. Cross-component: See **Section 1 (API Server)** — etcd issues always affect API server

---

### 9. Cluster Upgrades

**Keywords**: `upgrade`, `update`, `cluster version`, `CVO`, `stuck`, `failed upgrade`, `progressing`

**Upgrade stuck / failed / operators degraded during upgrade:**

1. `cluster-scoped-resources/config.openshift.io/clusterversions/`
   → Upgrade status, target version, history
2. `cluster-scoped-resources/config.openshift.io/clusteroperators.yaml`
   → Which operators are blocking
3. `namespaces/openshift-cluster-version/pods/cluster-version-operator-*/<container>/<container>/logs/current.log`
   → CVO logs, payload application
4. `namespaces/openshift-cluster-version/core/events.yaml`
   → CVO events
5. `namespaces/openshift-<degraded-operator>/core/events.yaml`
   → Why specific operator failed to upgrade
6. `namespaces/openshift-<degraded-operator>/pods/*/<container>/<container>/logs/current.log`
   → Operator logs during upgrade

---

### 10. Workload Issues

**Keywords**: `deployment`, `replica`, `rollout`, `statefulset`, `daemonset`, `job`, `cronjob`, `scaling`, `not ready`

**Deployment not rolling out / replicas not ready:**

1. `namespaces/<namespace>/apps/deployments.yaml`
   → Deployment spec, status, conditions
2. `namespaces/<namespace>/apps/replicasets.yaml`
   → ReplicaSet status (owned by Deployment)
3. `namespaces/<namespace>/core/events.yaml`
   → Deployment/ReplicaSet events
4. `namespaces/<namespace>/core/pods.yaml`
   → Pod status (why pods aren't ready)

**StatefulSet issues:**

5. `namespaces/<namespace>/apps/statefulsets.yaml`
6. `namespaces/<namespace>/core/persistentvolumeclaims.yaml` (for PVC binding)

**DaemonSet not on all nodes:**

7. `namespaces/<namespace>/apps/daemonsets.yaml`
8. `cluster-scoped-resources/core/nodes/*.yaml` (check node taints/labels)

**Job / CronJob not running:**

9. `namespaces/<namespace>/batch/jobs.yaml`
10. `namespaces/<namespace>/batch/cronjobs.yaml`

---

### 11. Image Registry Issues

**Keywords**: `image pull`, `registry`, `ImagePullBackOff`, `image`, `registry unavailable`

**Image pull failures / registry unavailable:**

1. `cluster-scoped-resources/config.openshift.io/images.yaml`
   → Registry sources, allowed registries
2. `cluster-scoped-resources/config.openshift.io/proxies.yaml`
   → Corporate proxy / TLS inspection affecting pulls
3. `namespaces/openshift-image-registry/pods/image-registry-*/<container>/<container>/logs/current.log`
   → Registry logs
4. `namespaces/openshift-image-registry/core/events.yaml`
   → Registry pod issues
5. `cluster-scoped-resources/imageregistry.operator.openshift.io/`
   → Registry operator config
6. `namespaces/<namespace>/core/events.yaml`
   → ImagePullBackOff events with details
7. `host_service_logs/masters|workers/crio_service.log`
   → Runtime pull / x509 errors
8. `host_service_logs/masters|workers/kubelet_service.log`
   → Kubelet image pull failures

---

### 12. Monitoring / Alerts

**Keywords**: `prometheus`, `alertmanager`, `alert`, `metrics`, `monitoring`, `grafana`, `scrape`, `firing`

**Prometheus not scraping / alerts not firing / metrics missing:**

1. `namespaces/openshift-monitoring/pods/prometheus-k8s-*/<container>/<container>/logs/current.log`
   → Prometheus logs (scrape errors)
2. `namespaces/openshift-monitoring/pods/alertmanager-main-*/<container>/<container>/logs/current.log`
   → Alertmanager logs
3. `monitoring/prometheus/rules.json`
   → Prometheus recording and alerting rules
4. `monitoring/alertmanager/status.json`
   → Alertmanager config, silences
5. `namespaces/<namespace>/monitoring.coreos.com/servicemonitors.yaml`
   → ServiceMonitor definitions (scrape config)
6. `monitoring/metrics/metrics.openmetrics` (Conditional - requires gather_metrics)
   → Full metrics dump

---

### 13. Security & Audit

**Keywords**: `audit`, `security`, `rbac`, `certificate`, `csr`, `scc`, `security context`

1. `audit_logs/kube-apiserver/<node-name>-audit.log` (Conditional)
2. `audit_logs/openshift-apiserver/<node-name>-audit.log` (Conditional)
3. `audit_logs/oauth-apiserver/<node-name>-audit.log` (Conditional)
4. `cluster-scoped-resources/rbac.authorization.k8s.io/`
5. `cluster-scoped-resources/security.openshift.io/securitycontextconstraints.yaml`
6. `namespaces/<namespace>/rbac.authorization.k8s.io/roles.yaml` and `rolebindings.yaml`

---

### 14. Storage Version Migration

**Keywords**: `kube-storage-version-migrator`, `KubeStorageVersionMigrator_Deploying`, `Available=False`, `migration`

1. `namespaces/openshift-kube-storage-version-migrator/core/events.yaml`
2. `namespaces/openshift-kube-storage-version-migrator/pods/*/logs/current.log` and `previous.log`
3. `cluster-scoped-resources/migration.k8s.io/storageversionmigrations.yaml`
4. `namespaces/openshift-kube-storage-version-migrator/apps/deployments.yaml`, `batch/jobs.yaml`
5. Cross: `namespaces/openshift-cluster-version/`, `etcd_info/`, `namespaces/openshift-kube-apiserver/`

---

### 15. IPsec & Network Security

**Keywords**: `ipsec`, `encryption`, `libreswan`, `xfrm`, `tunnel`, `traffic with IPsec`

1. `network_logs/ipsec/status/`, `network_logs/ipsec/trafficstatus/`, `network_logs/ipsec/xfrm/`
2. `network_logs/ipsec/<pod-name>_ipsec.conf`, `<pod-name>_libreswan.log`
3. `pod_network_connectivity_check/podnetworkconnectivitychecks.yaml`
4. Cross: `namespaces/openshift-ovn-kubernetes/`, `namespaces/openshift-network-operator/`

### 16. External DNS / API Resolution (Infrastructure)

**Keywords**: `external DNS`, `api-int`, `no such host`, `NXDOMAIN`, `VIP`, `NotReady master`, `API unreachable`

1. `cluster-scoped-resources/config.openshift.io/infrastructures.yaml`
2. `cluster-scoped-resources/config.openshift.io/dnses.yaml`
3. `pod_network_connectivity_check/podnetworkconnectivitychecks.yaml`
4. `host_service_logs/masters/kubelet_service.log`
5. CoreDNS events/logs under `namespaces/openshift-dns/`

### 17. Enterprise Proxy / TLS Trust

**Keywords**: `proxy`, `x509`, `unknown authority`, `ImagePullBackOff`, `additionalTrustBundle`

1. `proxies.yaml`, `images.yaml`
2. kubelet + crio service logs
3. `namespaces/openshift-image-registry/` when pull-related

### 18. Machine API / Node Provisioning

**Keywords**: `machine api`, `machineset`, `node not joining`, `MachineHealthCheck`, `machine not provisioned`

1. `namespaces/openshift-machine-api/core/events.yaml` + pod logs
2. `cluster-scoped-resources/machine.openshift.io/machines/` (Machine CRs with providerStatus/conditions)
3. `cluster-scoped-resources/machine.openshift.io/machinesets/` (desired vs current replicas)
4. `cluster-scoped-resources/machine.openshift.io/machinehealthchecks/` (if MHC-related)
5. `cluster-scoped-resources/core/nodes/*.yaml`
6. `infrastructures.yaml`

### 19. Ingress / Routes

**Keywords**: `ingress`, `route`, `haproxy`, `*.apps`

1. `ingress_controllers/*/haproxy.config`
2. `namespaces/openshift-ingress/` and `openshift-ingress-operator/` logs/events
3. `infrastructures.yaml` + `dnses.yaml`

### 20. Cluster Upgrade / CVO

**Keywords**: `upgrade`, `CVO`, `stuck update`, `Upgradeable=False`

1. `clusterversions.yaml` + `clusteroperators.yaml`
2. `namespaces/openshift-cluster-version/` events + logs
3. MCP when drain blocked

### 21. Workloads

**Keywords**: `deployment`, `statefulset`, `daemonset`, `job`, `rollout`

1. namespace `apps/*.yaml` + `batch/*.yaml`
2. `core/events.yaml`, `core/pods.yaml`
3. failing pod current.log + previous.log

### 22. Scheduler / Controllers

**Keywords**: `FailedScheduling`, `Pending`, `scheduler`

1. `namespaces/openshift-kube-scheduler/` logs/events
2. `schedulers.yaml`, nodes/
3. `openshift-kube-controller-manager/` when replicas stuck

### 23. Admission Webhooks

**Keywords**: `webhook`, `admission`, `validating`, `mutating`, `MutatingAdmissionWebhook`, `failed to complete mutation`, `timeoutSeconds`

1. `cluster-scoped-resources/admissionregistration.k8s.io/mutatingwebhookconfigurations/` — **ALL** CRs
2. `cluster-scoped-resources/admissionregistration.k8s.io/validatingwebhookconfigurations/` — **ALL** CRs
3. For each webhook: record `timeoutSeconds`, `failurePolicy`, service namespace/name; **match** any `Ns` in the user error to `timeoutSeconds: N`
4. Endpoints/EndpointSlices for each webhook service (zero endpoints = dead backend)
5. Webhook namespace pod logs + events (discover namespaces from CR `clientConfig`, including vault/dynatrace/otel/devworkspace/CI/security injectors)
6. kube-apiserver audit/logs only as supporting dial/timeout evidence — not a substitute for full CR inventory
7. Prefer remove/disable/fix failing webhooks as primary remediation; control-plane cascade is secondary unless webhooks are healthy

### 24. RHOSO / OpenStack

**Keywords**: `RHOSO`, `Nova`, `Galera`, `RabbitMQ`, `Keystone`, `openstack`

1. Apply External DNS / API set first if masters NotReady
2. `namespaces/openstack/` events + service pod logs
3. clusteroperators + infrastructures/dnses/proxies/images

### 25. Insights / Compliance

**Keywords**: `insights`, `compliance`

1. `insights-data/`
2. `namespaces/openshift-insights/` logs/events

### 26. KubeletConfig / SystemMemoryExceedsReservation

**Keywords**: `SystemMemoryExceedsReservation`, `autoSizingReserved`, `KubeletConfig`, `systemReserved`, `kubeReserved`, `auto-sizing`, `memory reservation`

**CHECK FIRST (before monitoring/Prometheus):**

1. `cluster-scoped-resources/machineconfiguration.openshift.io/kubeletconfigs/` (or `kubeletconfigs.yaml`)
   → Validate `spec.autoSizingReserved` placement (NOT under `spec.kubeletConfig`)
2. `cluster-scoped-resources/machineconfiguration.openshift.io/machineconfigs.yaml`
   → Including `*auto-sizing*` MachineConfigs (filenames alone are not root cause)
3. `cluster-scoped-resources/machineconfiguration.openshift.io/machineconfigpools.yaml`
4. `host_service_logs/masters|workers/kubelet_service.log`
5. `cluster-scoped-resources/core/nodes/*.yaml` → capacity vs allocatable
6. `machine_config_ondisk/<node>/mcs-machine-config-content.json` when present

**Only after KubeletConfig is correct:** monitoring Prometheus/cAdvisor, workload OOM, upgrade churn.

### 27. OLM / OperatorHub / Subscriptions

**Keywords**: `OLM`, `OperatorHub`, `Subscription`, `CatalogSource`, `InstallPlan`, `CSV`, `ClusterServiceVersion`, `operator install`, `marketplace`, `catalogd`

1. `namespaces/openshift-operator-lifecycle-manager/` logs/events
2. `namespaces/openshift-marketplace/` logs/events (CatalogSource pods)
3. `namespaces/<operator-namespace>/operators.coreos.com/subscriptions.yaml`, `installplans.yaml`, `clusterserviceversions.yaml`
4. `cluster-scoped-resources/apiextensions.k8s.io/customresourcedefinitions/` (CRDs)
5. `clusteroperators.yaml` (marketplace operator status)

### 28. Console / FeatureGate

**Keywords**: `console`, `web console`, `FeatureGate`, `TechPreview`, `TechPreviewNoUpgrade`, `console URL`, `console login`

1. `cluster-scoped-resources/config.openshift.io/consoles.yaml` (console URL, OAuth redirect)
2. `cluster-scoped-resources/config.openshift.io/featuregates.yaml` (enabled features, TechPreviewNoUpgrade)
3. `namespaces/openshift-console/` logs/events
4. `namespaces/openshift-console-operator/` logs/events
5. `authentications.yaml` (console login depends on OAuth)
6. `infrastructures.yaml` + `dnses.yaml` (console route DNS)

---

## Keyword to Directory Mapping with Prioritization

### API & Authentication
- **Primary**: `api server`, `apiserver`, `kube-apiserver` → `audit_logs/kube-apiserver/`, `namespaces/openshift-kube-apiserver/`
- **Secondary**: `openshift-apiserver` → `audit_logs/openshift-apiserver/`, `namespaces/openshift-apiserver/`
- **Tertiary**: `oauth`, `authentication`, `login` → `audit_logs/oauth-apiserver/`, `audit_logs/oauth-server/`, `namespaces/openshift-authentication/`
- **Specialized**: `api priority`, `fairness`, `throttling` → `namespaces/openshift-kube-apiserver/pods/*/api_priority_and_fairness/`
- **Critical Events**: `startup`, `termination`, `crash` (api server) → `static-pods/kube-apiserver/`

### Cluster & Operators
- **Primary**: `cluster operator`, `operator degraded` → `cluster-scoped-resources/config.openshift.io/clusteroperators.yaml`
- **Secondary**: `cluster version`, `upgrade`, `update` → `namespaces/openshift-cluster-version/`
- **Tertiary**: `olm`, `operator lifecycle` → `namespaces/openshift-operator-lifecycle-manager/`

### Networking
- **Primary (infra first)**: `api-int`, `no such host`, `NXDOMAIN`, `apiServerURL`, `external DNS`, `VIP DNS`, `NotReady master` → `infrastructures.yaml` + `dnses.yaml` + kubelet logs + `pod_network_connectivity_check/`
- **Primary (CNI)**: `network connectivity`, `pod network` → `pod_network_connectivity_check/`, `network_logs/` (after DNS/API checked)
- **Secondary**: `ovn`, `ovn-kubernetes` → `network_logs/ovnk_database_store.tar.gz`, `namespaces/openshift-ovn-kubernetes/`
- **OVN alerts**: `OVNKubernetesResourceRetryFailure`, `bz-networking` → OVN pod logs + `monitoring/alertmanager/`, `monitoring/prometheus/`
- **DNS (internal)**: `dns`, `coredns`, `svc.cluster.local`, `resolve` → `namespaces/openshift-dns/` + `dnses.yaml`
- **DNS (external)**: see Primary (infra first) above
- **Proxy / TLS**: `proxy`, `x509`, `unknown authority`, `ImagePullBackOff` → `proxies.yaml` + `images.yaml` + kubelet/crio
- **Ingress**: `ingress`, `route`, `haproxy` → `ingress_controllers/`, `namespaces/openshift-ingress/`, `namespaces/openshift-ingress-operator/`
- **Specialized**: `ipsec` → `network_logs/ipsec/`; `sriov` → `namespaces/openshift-sriov-network-operator/`; `metallb` → `namespaces/openshift-metallb-operator/`; `multus` → `namespaces/openshift-multus/`
- **Machine API**: `machineset`, `machine api`, `node not joining` → `namespaces/openshift-machine-api/`

### Storage
- **Primary**: `pvc`, `mount`, `volume attach` → `namespaces/*/core/persistentvolumeclaims.yaml`, `cluster-scoped-resources/storage.k8s.io/volumeattachments/`
- **Secondary**: `storage class`, `pv` → `cluster-scoped-resources/storage.k8s.io/storageclasses.yaml`, `cluster-scoped-resources/core/persistentvolumes/`
- **CSI**: `csi`, `csi driver` → `namespaces/openshift-cluster-csi-drivers/`, `cluster-scoped-resources/storage.k8s.io/csinodes.yaml`

### Nodes & Machines
- **Primary**: `node not ready`, `node status` → `cluster-scoped-resources/core/nodes/*.yaml`, `host_service_logs/`
- **Kernel/Hardware**: `oom`, `kernel`, `hardware` → `nodes/<node-name>/dmesg`
- **System Info**: `disk full`, `uptime`, `processes` → `nodes/<node-name>/sysinfo.log`
- **Machine Config**: `mco`, `machine config` → `namespaces/openshift-machine-config-operator/`, `machine_config_ondisk/`, `cluster-scoped-resources/machineconfiguration.openshift.io/`
- **KubeletConfig / memory reservation**: `SystemMemoryExceedsReservation`, `autoSizingReserved`, `KubeletConfig`, `systemReserved`, `kubeReserved` → `machineconfiguration.openshift.io/kubeletconfigs/` FIRST, then machineconfigs; monitoring only after field placement validated
- **Services**: `kubelet` → `host_service_logs/*/kubelet_service.log`; `crio` → `host_service_logs/*/crio_service.log`

### Pods & Containers
- **Primary**: `pod crash`, `container restart`, `pod pending` → `namespaces/<namespace>/pods/<pod-name>/<container>/<container>/logs/`
- **Secondary**: `pod events`, `scheduling` → `namespaces/<namespace>/core/events.yaml`
- **Workloads**: `deployment` → `apps/deployments.yaml`; `daemonset` → `apps/daemonsets.yaml`; `statefulset` → `apps/statefulsets.yaml`; `job` → `batch/jobs.yaml`; `cronjob` → `batch/cronjobs.yaml`

### etcd
- **Primary**: `etcd health`, `quorum` → `etcd_info/endpoint_health.json`, `etcd_info/member_list.json`
- **Alarms**: `etcd alarm`, `NOSPACE`, `CORRUPT` → `etcd_info/alarm_list.json`
- **Performance**: `etcdGRPCRequestsSlow`, `slow requests` → `etcd_info/` + `namespaces/openshift-etcd/` + `monitoring/metrics/metrics.openmetrics` + `nodes/`
- **Logs**: `etcd logs` → `namespaces/openshift-etcd/pods/*/logs/`, `audit_logs/etcd/`

### Image & Registry
- **Primary**: `image pull`, `ImagePullBackOff`, `registry` → `namespaces/openshift-image-registry/`, `cluster-scoped-resources/config.openshift.io/images.yaml`

### Monitoring
- **Primary**: `prometheus`, `alertmanager`, `alert` → `monitoring/prometheus/`, `monitoring/alertmanager/`, `namespaces/openshift-monitoring/`
- **Scrape config**: `servicemonitor` → `namespaces/<namespace>/monitoring.coreos.com/servicemonitors.yaml`

### Admission & Webhooks
- **Primary**: `MutatingAdmissionWebhook`, `failed to complete mutation`, `webhook timeout`, `timeoutSeconds` → ALL `admissionregistration.k8s.io/mutatingwebhookconfigurations/` + `validatingwebhookconfigurations/`; match error duration to `timeoutSeconds`; endpoints per webhook service
- **Remediation bias**: remove/disable/fix failing webhooks first; apiserver/OVN/RBAC cascade only if webhook inventory is healthy

### OLM / OperatorHub
- **Primary**: `OLM`, `OperatorHub`, `Subscription`, `CatalogSource`, `InstallPlan`, `CSV`, `marketplace` → `namespaces/openshift-operator-lifecycle-manager/`, `namespaces/openshift-marketplace/`
- **Secondary**: `operators.coreos.com/subscriptions.yaml`, `installplans.yaml`, `clusterserviceversions.yaml` in the target operator namespace
- **CRDs**: `cluster-scoped-resources/apiextensions.k8s.io/customresourcedefinitions/`

### Console / FeatureGate
- **Primary**: `console`, `web console`, `console URL`, `console login` → `config.openshift.io/consoles.yaml`, `namespaces/openshift-console/`, `namespaces/openshift-console-operator/`
- **FeatureGate**: `FeatureGate`, `TechPreview`, `TechPreviewNoUpgrade` → `config.openshift.io/featuregates.yaml`; also check upgrade docs (FeatureGate can block upgrades)
- **Cross**: `authentications.yaml` (console OAuth), `infrastructures.yaml` + `dnses.yaml` (route DNS)

### NMState / Multus / EgressIP (secondary network CRs)
- **NMState**: `nodenetworkstate`, `nodenetworkconfigurationpolicy`, `NMState` → `cluster-scoped-resources/nmstate.io/`
- **Multus**: `net-attach-def`, `multus`, `additional network`, `ippool` → `cluster-scoped-resources/k8s.cni.cncf.io/`
- **EgressIP**: `egressip`, `egress IP` → `cluster-scoped-resources/k8s.ovn.org/egressips/`
- **UDN**: `user-defined network`, `clusteruserdefinednetwork` → `cluster-scoped-resources/k8s.ovn.org/clusteruserdefinednetworks/`

---

## Cross-Reference Dependencies

### etcd Issues Must Include:
- **Mandatory**: `etcd_info/` + `namespaces/openshift-etcd/` + `namespaces/openshift-kube-apiserver/`
- **Related**: `audit_logs/etcd/` + `audit_logs/kube-apiserver/` + `monitoring/metrics/`

### API Server Issues Must Include:
- **Mandatory**: `namespaces/openshift-kube-apiserver/` + `audit_logs/kube-apiserver/`
- **Related**: `static-pods/kube-apiserver/` + `etcd_info/` + `monitoring/prometheus/`

### Network Issues Must Include:
- **Mandatory first**: `infrastructures.yaml` + `dnses.yaml` + `pod_network_connectivity_check/` when API/NotReady/DNS symptoms exist
- **Mandatory CNI**: `network_logs/` + `namespaces/openshift-ovn-kubernetes/` OR `namespaces/openshift-sdn/` when CNI implicated
- **Related**: `namespaces/openshift-dns/`; add `proxies.yaml`/`images.yaml` for x509/ImagePull
- **OVN alerts**: add `monitoring/alertmanager/`, `monitoring/prometheus/`

### Node Issues Must Include:
- **Mandatory**: `cluster-scoped-resources/core/nodes/*.yaml` + `host_service_logs/` + `nodes/<node-name>/*` (bare `nodes/<node-name>/` does not resolve to any file — use the trailing `*`)
- **Masters NotReady**: also Section external DNS/API files (`infrastructures`, `dnses`, connectivity checks)
- **Related**: `namespaces/openshift-machine-config-operator/`; Machine API namespace when provision/join failures

### Pod Issues Must Include:
- **Mandatory**: `namespaces/<namespace>/pods/<pod-name>/<container>/<container>/logs/` + `namespaces/<namespace>/core/events.yaml`
- **Related**: `host_service_logs/` + `nodes/<node-name>/dmesg` (for OOMKilled)

### Upgrade Issues Must Include:
- **Mandatory**: `cluster-scoped-resources/config.openshift.io/clusterversions/` + `clusteroperators.yaml` + `namespaces/openshift-cluster-version/`
- **Related**: Logs from any degraded operator namespace

### Loss of APIServer + etcd quorum + high CPU (mass test failure):
- **Mandatory**: API server + etcd + networking + `monitoring/metrics/metrics.openmetrics`, `nodes/*/*`, `host_service_logs/masters/kubelet_service.log`, `cluster-scoped-resources/config.openshift.io/clusteroperators.yaml`

### OLM / Operator Install Issues Must Include:
- **Mandatory**: `namespaces/openshift-operator-lifecycle-manager/` + `namespaces/openshift-marketplace/`
- **Related**: `operators.coreos.com/subscriptions.yaml`, `installplans.yaml`, `clusterserviceversions.yaml` in operator namespace + CRDs

### Console / FeatureGate Issues Must Include:
- **Mandatory**: `config.openshift.io/consoles.yaml` + `config.openshift.io/featuregates.yaml` + `namespaces/openshift-console/` + `namespaces/openshift-console-operator/`
- **Related**: `authentications.yaml` (OAuth), `infrastructures.yaml` + `dnses.yaml` (route DNS), Ingress files when console route is unreachable
- **Upgrade cross-ref**: `featuregates.yaml` may block upgrades (TechPreviewNoUpgrade)

### Storage Issues Must Also Include:
- **PVCs**: `namespaces/<namespace>/core/persistentvolumeclaims.yaml` (affected namespace)
- **CSI driver pods**: `namespaces/openshift-cluster-csi-drivers/pods/*/logs/`
- **Volume snapshots** (conditional): `cluster-scoped-resources/snapshot.storage.k8s.io/`

---

## Quick Reference: File Type Guide

| File/Dir Pattern | Contains | When to Use |
|------------------|----------|-------------|
| `events.yaml` | All events (errors, warnings, info) | ★ Always check first — human-readable errors |
| `pods.yaml` | All pod specs & status (aggregated) | Pod issues, resource limits, scheduling |
| `clusteroperators.yaml` | Operator health matrix | ★ First file for cluster health |
| `clusterversions.yaml` | Version & upgrade state | Upgrade issues, version mismatch |
| `nodes/<node>.yaml` | Node conditions, capacity | Node NotReady, resource exhaustion |
| `machineconfigs/` | OS configurations | Node config changes (compare rendered-*) |
| `current.log` | Active container logs | Application errors, runtime issues |
| `previous.log` | Crashed container logs | CrashLoopBackOff, OOMKilled |
| `*_service.log` | Systemd service logs | Low-level system services (kubelet, CRI-O) |
| `*_logs_kubelet.gz` | Compressed kubelet logs | Pod lifecycle, mount failures |
| `dmesg` | Kernel ring buffer | OOM kills, hardware faults, kernel panics |
| `sysinfo.log` | System info (df, ps, uptime) | Disk/memory/CPU pressure |
| `etcd_info/*.json` | Etcd cluster health | Quorum, performance, storage |
| `ovnk_database_store.tar.gz` | OVN flow rules | Deep network troubleshooting |
| `event-filter.html` | Web UI for all events | Search all events across cluster |
| `metrics.openmetrics` | Full metrics dump | Performance analysis (large file) |
| `haproxy.config` | HAProxy routing config | Ingress routing issues |

---

## Common Patterns to Recognize

### Resource Name Patterns
- `rendered-master-<hash>` / `rendered-worker-<hash>` → Applied MachineConfig (compare hashes for drift)
- `00-*`, `01-*`, `97-*`, `98-*`, `99-*` → MachineConfig priority (higher number = applied later)
- `installer-*` → Static pod installer jobs
- `revision-pruner-*` → Cleanup jobs for old revisions

### Event Reasons (in events.yaml)
- `FailedScheduling` → Node capacity, affinity, taints
- `ImagePullBackOff` → Registry, credentials, network
- `CrashLoopBackOff` → Check `previous.log`
- `OOMKilled` → Memory limit too low
- `Unhealthy` → Liveness/readiness probe failing
- `FailedMount` → Storage issue (PVC, CSI)
- `BackOff` → Container start failed repeatedly
- `Killing` → Container being terminated

### Operator Conditions (in clusteroperators.yaml)
- `Available=False` → Operator not working
- `Degraded=True` → Partial failure
- `Progressing=True` → Upgrade/rollout in progress
- `Upgradeable=False` → Blocks upgrades

### Node Conditions (in nodes/*.yaml)
- `Ready=False` → Node unhealthy
- `MemoryPressure=True` → Low memory
- `DiskPressure=True` → Low disk
- `PIDPressure=True` → Too many processes

---

## Aggregated Resource Files

Many resource types are collected into a single aggregated YAML file per namespace:
- `namespaces/<namespace>/core/pods.yaml` — contains **all** pod definitions (not one file per pod)
- `namespaces/<namespace>/apps/deployments.yaml` — contains **all** deployments
- `namespaces/<namespace>/core/services.yaml` — contains **all** services
- `cluster-scoped-resources/config.openshift.io/clusteroperators.yaml` — contains **all** ClusterOperators

**Per-object directories** (one YAML per object — use `*.yaml` glob, **not** a trailing `/` alone):
- `cluster-scoped-resources/core/nodes/*.yaml` — one Node CR per file (`<node-name>.yaml`); **`core/nodes/` does not resolve**
- `cluster-scoped-resources/config.openshift.io/dnses.yaml` — cluster DNS config (always include for API/external DNS RCA)

Individual pod data (YAML + logs) is available under `namespaces/<namespace>/pods/<pod-name>/`. CoreDNS logs use the container path: `namespaces/openshift-dns/pods/*/*/*/logs/current.log`.

---

## Mandatory Inclusion Rules

### Always Include Both:
- **Current AND Previous Logs**: When analyzing pod issues, always include both `current.log` and `previous.log` as **two separate lines**
- **Pod Logs AND Events**: Always include both pod logs and namespace events
- **Node Status AND Service Logs**: Always include both node YAML and relevant service logs
- **Health AND Status**: For etcd, always include both `endpoint_health.json` and `member_list.json`

### Component Dependencies:
- **etcd Issues**: Always include API server logs; include infrastructures/dnses when dial/network path failures present
- **API Server Issues**: Always include etcd health; include infrastructures/dnses/connectivity when unreachable
- **Network Issues**: Always include connectivity checks + DNS (internal and external config) before OVN/CRI-O primacy
- **NotReady Masters**: Always include external DNS/API resolution set before OVN/CRI-O
- **ImagePull / x509**: Always include proxies.yaml + images.yaml
- **SystemMemoryExceedsReservation**: Always include kubeletconfigs + validate `autoSizingReserved` placement before monitoring primacy
- **MutatingAdmissionWebhook / webhook timeout**: Always inventory ALL webhook CRs; match `timeoutSeconds` to error; endpoints; prefer webhook fix over apiserver primary
- **Storage Issues**: Always include both pod logs and volume attachment status
- **Performance Issues**: Always include both metrics and node data
- **Upgrade Issues**: Always include clusterversions + clusteroperators + CVO logs
- **Machine not joining**: Always include openshift-machine-api events/logs

### Platform-Specific:
- **vSphere**: Include `namespaces/openshift-vsphere-csi-driver/` for storage issues
- **Windows Nodes**: Include `host_service_logs/windows/` for Windows-related issues
- **Service Mesh**: Include `istio/` for Istio-related issues

---

## Analysis Strategy for LLMs

### Step 1: Understand the Problem
- Parse user's problem statement
- Identify category (pod / node / network / storage / control-plane / upgrade / auth)
- Extract keywords (namespace, pod name, node name, operator name)

### Step 2: Start Broad
ALWAYS check these first:
1. `cluster-scoped-resources/config.openshift.io/clusteroperators.yaml`
2. `cluster-scoped-resources/config.openshift.io/clusterversions.yaml`
3. `event-filter.html` (or `namespaces/<relevant-namespace>/core/events.yaml`)

### Step 3: Narrow Down
- Use Decision Matrix above to find specific files for the problem category
- Check `events.yaml` in relevant namespace
- Read pod/container logs (`current.log` then `previous.log`)
- Correlate timestamps across files

### Step 4: Deep Dive
- Compare resource versions (e.g. `rendered-master-*` hashes)
- Extract error messages, stack traces
- Check resource utilization (`nodes/*/sysinfo.log`, `nodes/*/dmesg`)
- Verify configurations

### Step 5: Build Timeline
Extract timestamps from:
- `events.yaml` (`lastTimestamp`, `firstTimestamp`)
- Logs (log line timestamps)
- Resource YAMLs (`creationTimestamp`, `conditions.lastTransitionTime`)
- Correlate events across files to determine cause → effect chain

---

## Notes

- All paths are relative to `<must-gather-root>/<content-folder>/`
- Content folder is one child under root; name can be any string (e.g. quay-content)
- Some directories only exist if features are enabled (conditional)
- Some files are compressed on disk (`.gz`, `.log.gz`, `.tar.gz`). Always reference them by their actual on-disk name including the compression extension
- JSON/YAML files can be queried programmatically
- Log files are time-sensitive; check collection time window
- Follow mandatory inclusion rules to ensure comprehensive analysis
- Use cross-reference dependencies to identify related component issues
- Large files (audit logs, metrics.openmetrics) should only be parsed when the investigation specifically requires them

---
