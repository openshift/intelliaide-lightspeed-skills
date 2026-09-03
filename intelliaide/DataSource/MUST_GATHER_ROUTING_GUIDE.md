---
# Must-Gather Routing Guide for LLM Problem Diagnosis

This document provides a structured mapping of problem types to relevant directories and files in the must-gather output. Use this guide to route diagnostic queries to the appropriate data sources.

**Path convention**: The user supplies the **must-gather root** folder. Under it there is **one folder with any name** (e.g. `quay-content`—the name is not fixed). All paths in this guide are under `<must-gather-root>/<content-folder>/`; the tool resolves the content folder automatically.

**Path substitution rules**:
- `<namespace>` = actual namespace name (e.g. `openshift-etcd`)
- `<pod-name>` = actual pod name (e.g. `etcd-ip-10-0-122-129.us-east-2.compute.internal`)
- `<node-name>` = actual node name (e.g. `ip-10-0-122-129.us-east-2.compute.internal`)
- `*` = wildcard for any matching file/directory name
- Files marked as **MANDATORY** must always be included for that problem type

**Output convention for LLM**: When listing paths in your response, use **`pods/*/logs/current.log`** and **`pods/*/logs/previous.log`** (and similarly **`*`** for node/pod where many exist). Do not output literal `<pod-name>` or `<node-name>`.

## Problem Category Index

### 1. API Server & Authentication Issues
### 2. Cluster Operator & Control Plane Issues
### 3. Networking & Connectivity Issues
### 4. Storage & Volume Issues
### 5. Node & Machine Configuration Issues
### 6. Pod & Container Issues
### 7. Performance & Resource Issues
### 8. Security & Audit Issues
### 9. Service Mesh & Istio Issues
### 10. Monitoring & Metrics Issues
### 11. Windows Node Issues
### 12. Platform-Specific Issues (vSphere, ARO, etc.)
### 13. etcd Issues
### 14. Storage Version Migration Issues
### 15. IPsec & Network Security Issues
### 16. External DNS / API Resolution (infrastructure)
### 17. Enterprise Proxy / Image Pull / TLS Trust
### 18. Machine API / Node Provisioning
### 19. Image Registry Issues

### 20. Ingress / Routes
### 21. Cluster Upgrade / CVO
### 22. Workloads (Deployments / Jobs)
### 23. Scheduler / Controller Manager
### 24. Admission Webhooks
### 25. RHOSO / OpenStack on OpenShift
### 26. Insights / Compliance
### 27. KubeletConfig / SystemMemoryExceedsReservation
### 28. OLM / OperatorHub / Subscriptions
### 29. Console / FeatureGate

---

## 1. API Server & Authentication Issues

**Keywords**: `api server`, `apiserver`, `authentication`, `authorization`, `oauth`, `kube-apiserver`, `openshift-apiserver`, `api calls`, `api requests`, `401`, `403`, `unauthorized`, `forbidden`, `api rate limiting`, `throttling`, `api unreachable`, `503`, `timeout`, `no such host`

### Primary Files (MANDATORY):
- **`cluster-scoped-resources/config.openshift.io/infrastructures.yaml`** (API URLs that must resolve in external DNS)
- **`cluster-scoped-resources/config.openshift.io/dnses.yaml`** (cluster domain + upstream DNS)
- **`pod_network_connectivity_check/podnetworkconnectivitychecks.yaml`**
- **`audit_logs/kube-apiserver/<node-name>-audit.log`** (Conditional) (all master nodes)
- **`namespaces/openshift-kube-apiserver/pods/<pod-name>/<container-name>/<container-name>/logs/current.log`** (all API server pods)
- **`namespaces/openshift-kube-apiserver/pods/<pod-name>/<container-name>/<container-name>/logs/previous.log`** (all API server pods)
- **`namespaces/openshift-kube-apiserver/core/events.yaml`**

### API Priority and Fairness (for throttling issues):
- **`namespaces/openshift-kube-apiserver/pods/<pod-name>/kube-apiserver/kube-apiserver/api_priority_and_fairness/priority_levels`**
- **`namespaces/openshift-kube-apiserver/pods/<pod-name>/kube-apiserver/kube-apiserver/api_priority_and_fairness/queues`**
- **`namespaces/openshift-kube-apiserver/pods/<pod-name>/kube-apiserver/kube-apiserver/api_priority_and_fairness/requests`**

### OpenShift API Server:
- **`audit_logs/openshift-apiserver/<node-name>-audit.log`** (Conditional)
- **`namespaces/openshift-apiserver/pods/<pod-name>/<container-name>/<container-name>/logs/current.log`**
- **`namespaces/openshift-apiserver/pods/<pod-name>/<container-name>/<container-name>/logs/previous.log`**

### OAuth & Authentication:
- **`cluster-scoped-resources/config.openshift.io/authentications/`** (or authentications.yaml)
- **`cluster-scoped-resources/config.openshift.io/oauths.yaml`**
- **`cluster-scoped-resources/config.openshift.io/proxies.yaml`** (when external IdP may be blocked)
- **`audit_logs/oauth-apiserver/<node-name>-audit.log`** (Conditional)
- **`audit_logs/oauth-server/<node-name>-audit.log`** (Conditional)
- **`namespaces/openshift-authentication/pods/<pod-name>/<container-name>/<container-name>/logs/current.log`**
- **`namespaces/openshift-authentication/pods/<pod-name>/<container-name>/<container-name>/logs/previous.log`**
- **`namespaces/openshift-authentication/core/events.yaml`**
- **`namespaces/openshift-oauth-apiserver/pods/<pod-name>/<container-name>/<container-name>/logs/current.log`**
- **`namespaces/openshift-oauth-apiserver/pods/<pod-name>/<container-name>/<container-name>/logs/previous.log`**

### Static Pod Issues:
- **`static-pods/kube-apiserver/<node-name>-startup.log.gz`** (compressed)
- **`static-pods/kube-apiserver/<node-name>-termination.log.gz`** (compressed)

### Cross-Component Dependencies:
- **`host_service_logs/masters/kubelet_service.log`** (for API server pod issues)
- **`etcd_info/endpoint_health.json`** (API server depends on etcd)
- **`cluster-scoped-resources/config.openshift.io/apiservers.yaml`**

> **Note on audit logs**: All `audit_logs/*` entries are conditional — they are only present when audit log collection succeeds and the corresponding API server is running.

---

## 2. Cluster Operator & Control Plane Issues

**Keywords**: `cluster operator`, `operator`, `control plane`, `degraded`, `available`, `progressing`, `cluster version`, `upgrade`, `update`, `operator failure`, `operator crash`

### Primary Files (MANDATORY):
- **`cluster-scoped-resources/config.openshift.io/clusteroperators.yaml`**
- **`namespaces/openshift-cluster-version/core/events.yaml`**
- **`namespaces/openshift-cluster-version/pods/<pod-name>/logs/current.log`**
- **`namespaces/openshift-cluster-version/pods/<pod-name>/logs/previous.log`**

### Operator-Specific Namespaces:
- **`namespaces/<operator-namespace>/pods/<pod-name>/logs/current.log`**
- **`namespaces/<operator-namespace>/pods/<pod-name>/logs/previous.log`**
- **`namespaces/<operator-namespace>/core/events.yaml`**

### OLM (Operator Lifecycle Manager):
- **`namespaces/openshift-operator-lifecycle-manager/pods/<pod-name>/logs/current.log`**
- **`namespaces/openshift-operator-lifecycle-manager/pods/<pod-name>/logs/previous.log`**
- **`namespaces/openshift-catalogd/pods/<pod-name>/logs/current.log`**
- **`namespaces/openshift-catalogd/pods/<pod-name>/logs/previous.log`**

### Cross-Component Dependencies:
- **`cluster-scoped-resources/config.openshift.io/clusterversions.yaml`**
- **`cluster-scoped-resources/operator.openshift.io/`** (all operator configs)
- **`host_service_logs/masters/machine-config-daemon-firstboot_service.log`**
- **`host_service_logs/masters/machine-config-daemon-host_service.log`**

---

## 3. Networking & Connectivity Issues

**Keywords**: `network`, `networking`, `connectivity`, `pod network`, `service network`, `route`, `ingress`, `egress`, `dns`, `load balancer`, `multus`, `sdn`, `ovn`, `network policy`, `egress firewall`, `node network`, `interface`, `bridge`, `OVNKubernetesResourceRetryFailure`, `component readiness`, `alert`, `invariant`, `bz-networking`, `api unreachable`, `NotReady`, `no such host`, `NXDOMAIN`, `api-int`, `external DNS`, `VIP`

### Primary Files (MANDATORY) — check DNS/API resolution BEFORE OVN/CRI-O:
- **`cluster-scoped-resources/config.openshift.io/infrastructures.yaml`**
- **`cluster-scoped-resources/config.openshift.io/dnses.yaml`**
- **`pod_network_connectivity_check/podnetworkconnectivitychecks.yaml`**
- **`network_logs/cluster_scale`**
- **`cluster-scoped-resources/config.openshift.io/networks.yaml`**
- **`namespaces/openshift-dns/pods/*/*/*/logs/current.log`**
- **`namespaces/openshift-dns/pods/*/*/*/logs/previous.log`**
- **`namespaces/openshift-dns/core/events.yaml`**

### OVN-Kubernetes (if using OVN):
For OVN issues, alerts, or component readiness (e.g. **OVNKubernetesResourceRetryFailure**, bz-networking invariant): include monitoring/alertmanager and OVN pod logs/events below.
- **`monitoring/alertmanager/`** (alert status and config)
- **`monitoring/prometheus/`** (alert rules and metrics)
- **`network_logs/leader_ovnnb_status`** (**legacy/single-zone OVN mode only** — absent in interconnect mode)
- **`network_logs/leader_ovnsb_status`** (**legacy/single-zone OVN mode only** — absent in interconnect mode)
- **`network_logs/ovn_kubernetes_top_pods`**
- **`network_logs/ovnk_database_store.tar.gz`** (compressed OVN database archive; per-node NB/SB pairs in interconnect mode)
- **`network_logs/ovnk_extras_store.tar.gz`** (**interconnect mode only** — per-node `libovsdb*.log` extras)
- **`namespaces/openshift-ovn-kubernetes/pods/<pod-name>/logs/current.log`**
- **`namespaces/openshift-ovn-kubernetes/pods/<pod-name>/logs/previous.log`**
- **`namespaces/openshift-ovn-kubernetes/core/events.yaml`**

> **OVN mode check**: Most current OpenShift clusters run OVN-Kubernetes in **interconnect mode** (one zone per node) by default — the `leader_*` files will not exist there; do not report their absence as a problem. Only clusters still on **legacy (single raft-clustered) mode** produce `leader_nbdb`/`leader_sbdb`/`leader_ovnnb_status`/`leader_ovnsb_status`.

### Network Operator:
- **`namespaces/openshift-network-operator/pods/<pod-name>/logs/current.log`**
- **`namespaces/openshift-network-operator/pods/<pod-name>/logs/previous.log`**
- **`namespaces/openshift-network-operator/core/events.yaml`**

### DNS — INTERNAL (CoreDNS / cluster DNS)
Use when pods cannot resolve *cluster* service names (`*.svc.cluster.local`), or `openshift-dns` pods are unhealthy.

- **`namespaces/openshift-dns/pods/*/*/*/logs/current.log`**
- **`namespaces/openshift-dns/pods/*/*/*/logs/previous.log`**
- **`namespaces/openshift-dns/core/events.yaml`**
- **`cluster-scoped-resources/config.openshift.io/dnses.yaml`**

### DNS — EXTERNAL / INFRASTRUCTURE (API resolution)
Use when nodes, kubelet, operators, or clients cannot resolve or reach `api.<cluster-domain>`, `api-int.<cluster-domain>`, or `*.apps.<cluster-domain>`. This is **outside** CoreDNS. Missing corporate/external DNS records, wrong upstream resolvers, or LB/VIP DNS gaps commonly cause: NotReady masters, kubelet lease failures, API timeouts, and cascading OpenStack (Nova) control-plane downs on RHOSO.

**Mandatory (HIGH):**
- **`cluster-scoped-resources/config.openshift.io/infrastructures.yaml`** → `apiServerURL`, `apiServerInternalURI`
- **`cluster-scoped-resources/config.openshift.io/dnses.yaml`** → cluster domain + upstream DNS
- **`pod_network_connectivity_check/podnetworkconnectivitychecks.yaml`**
- **`host_service_logs/masters/kubelet_service.log`** → `lookup`, `no such host`, dial failures to api/api-int
- **`host_service_logs/masters/NetworkManager_service.log`** → resolver/DNS client (often symptom, not root)
- CoreDNS files above (to **rule out** internal DNS)

**Causal rule:** If kubelet/API connectivity shows hostname lookup failures for api/api-int, do **not** promote OVN-SB, CRI-O, or etcd quorum as primary until external DNS / VIP resolution is confirmed. OVN/CRI-O/etcd noise is expected *after* API becomes unreachable.

See also **Section 16**.

### Ingress & Routes:
- **`ingress_controllers/default/<pod-name>/haproxy.config`**
- **`namespaces/openshift-ingress-operator/pods/<pod-name>/logs/current.log`**
- **`namespaces/openshift-ingress-operator/pods/<pod-name>/logs/previous.log`**

### SR-IOV (if enabled):
- **`namespaces/openshift-sriov-network-operator/pods/<pod-name>/logs/current.log`**
- **`namespaces/openshift-sriov-network-operator/pods/<pod-name>/netns`**
- **`namespaces/openshift-sriov-network-operator/pods/<pod-name>/ip_link`**
- **`namespaces/openshift-sriov-network-operator/pods/<pod-name>/ethtool`**

### MetalLB (if enabled):
- **`namespaces/openshift-metallb-operator/pods/<pod-name>/logs/current.log`**
- **`namespaces/openshift-metallb-operator/pods/<pod-name>/logs/previous.log`**

### FRR-K8s (if enabled):
- **`namespaces/openshift-frr-k8s/pods/<pod-name>/logs/current.log`**
- **`namespaces/openshift-frr-k8s/pods/<pod-name>/frr/frr/logs/frr.conf`**
- **`namespaces/openshift-frr-k8s/pods/<pod-name>/frr/frr/logs/dump_frr`**

### Secondary Network CRs (conditionally collected — include when present and relevant):
- **NMState**: `cluster-scoped-resources/nmstate.io/nodenetworkstates/`, `nodenetworkconfigurationpolicies/` (if NMState enabled)
- **Multus**: `cluster-scoped-resources/k8s.cni.cncf.io/net-attach-def/`, `ippools/`, `multi-networkpolicy/` (if Multus enabled)
- **OVN-K CRs**: `cluster-scoped-resources/k8s.ovn.org/egressips/`, `clusteruserdefinednetworks/` (if OVN enabled)
- **OpenShift SDN**: `cluster-scoped-resources/network.openshift.io/hostsubnets/` (if SDN mode)

### OVS Service Logs (when OVS/dataplane investigation needed):
- **`host_service_logs/masters/openvswitch_service.log`**, **`ovs-configuration_service.log`**, **`ovs-vswitchd_service.log`**, **`ovsdb-server_service.log`** (and workers/ equivalents)

### Cross-Component Dependencies:
- **`host_service_logs/masters/NetworkManager_service.log`**
- **`host_service_logs/workers/NetworkManager_service.log`**
- Container runtime (`crio_service.log`) — include when CNI/runtime is implicated; **do not** treat as mandatory primary for every networking symptom when external DNS/API resolution is the clearer fit

---

## 4. Storage & Volume Issues

**Keywords**: `storage`, `volume`, `pvc`, `pv`, `persistent volume`, `csi`, `storage class`, `mount`, `unmount`, `attach`, `detach`, `storage driver`, `vsphere`, `ceph`, `nfs`

### Primary Files (MANDATORY):
- **`cluster-scoped-resources/storage.k8s.io/storageclasses.yaml`**
- **`cluster-scoped-resources/core/persistentvolumes/<pv-name>.yaml`**
- **`cluster-scoped-resources/storage.k8s.io/volumeattachments/<attachment-name>.yaml`**
- **`namespaces/<namespace>/core/persistentvolumeclaims.yaml`**

### CSI Drivers:
- **`namespaces/openshift-cluster-csi-drivers/pods/<pod-name>/logs/current.log`**
- **`namespaces/openshift-cluster-csi-drivers/pods/<pod-name>/logs/previous.log`**
- **`cluster-scoped-resources/storage.k8s.io/csidrivers.yaml`**
- **`cluster-scoped-resources/storage.k8s.io/csinodes.yaml`**

### Storage Operator:
- **`namespaces/openshift-cluster-storage-operator/pods/<pod-name>/logs/current.log`**
- **`namespaces/openshift-cluster-storage-operator/pods/<pod-name>/logs/previous.log`**

### vSphere Storage (if applicable):
- **`namespaces/openshift-vsphere-csi-driver/pods/<pod-name>/logs/current.log`**
- **`cluster-scoped-resources/csinodetopologies.cns.vmware.com/<topology-name>.yaml`**

### Volume Snapshots (conditional — if snapshot controller enabled):
- **`cluster-scoped-resources/snapshot.storage.k8s.io/volumesnapshotclasses/`**
- **`cluster-scoped-resources/snapshot.storage.k8s.io/volumesnapshotcontents/`**

### Cross-Component Dependencies:
- **`namespaces/<namespace>/pods/<pod-name>/logs/current.log`** (for mount failures)
- **`namespaces/<namespace>/core/events.yaml`** (for storage events — FailedMount, FailedAttach, ProvisioningFailed)

---

## 5. Node & Machine Configuration Issues

**Keywords**: `node`, `machine`, `machine config`, `mco`, `machineconfig`, `node tuning`, `performance profile`, `kernel`, `boot`, `bootstrap`, `degraded node`, `not ready`, `NotReady`, `scheduling`, `taint`, `cordon`, `NodeStatusUnknown`, `lease`, `SystemMemoryExceedsReservation`, `autoSizingReserved`, `KubeletConfig`, `systemReserved`, `kubeReserved`

### Primary Files (MANDATORY):
- **`cluster-scoped-resources/core/nodes/<node-name>.yaml`**
- **`nodes/<node-name>/<node-name>_logs_kubelet.gz`** (compressed)
- **`host_service_logs/masters/kubelet_service.log`**
- **`host_service_logs/workers/kubelet_service.log`**
- **`nodes/<node-name>/*`** — wildcard to pull the full per-node diagnostic set in one shot (`dmesg`, `sysinfo.log`, `sysinfo.tgz`, `proc_cmdline`, `lscpu`, `lspci`, `ethtool_channels`, `ethtool_features`, `cpu_affinities.json`, `irq_affinities.json`, `podresources.json`, `pods_info.json`); a bare `nodes/<node-name>/` does **not** resolve to any file

### When masters are NotReady / NodeStatusUnknown (MANDATORY — apply BEFORE OVN/CRI-O):
Also include all **Section 16 (External DNS / API Resolution)** primary files. Master NotReady with lease renewal failures is frequently caused by API hostname resolution or API unreachability, not by CRI-O or OVN alone.

### SystemMemoryExceedsReservation / kubelet memory reservation (MANDATORY — BEFORE monitoring):
See **Section 27**. Always include KubeletConfig CRs and validate `autoSizingReserved` field placement before blaming Prometheus/cAdvisor or workload pressure.

### Machine Config Operator:
- **`namespaces/openshift-machine-config-operator/pods/<pod-name>/logs/current.log`**
- **`namespaces/openshift-machine-config-operator/pods/<pod-name>/logs/previous.log`**
- **`cluster-scoped-resources/machineconfiguration.openshift.io/machineconfigs.yaml`**
- **`cluster-scoped-resources/machineconfiguration.openshift.io/machineconfigpools.yaml`**
- **`cluster-scoped-resources/machineconfiguration.openshift.io/kubeletconfigs/`** (or `kubeletconfigs.yaml`) — KubeletConfig CRs (`autoSizingReserved`, `systemReserved`, `kubeReserved`)

### On-Disk Configuration:
- **`machine_config_ondisk/<node-name>/mcs-machine-config-content.json`** (Conditional - if degraded nodes)
- **`machine_config_ondisk/<node-name>/bootstrapconfigdiff`** (Conditional - if degraded nodes)

### Node Tuning:
- **`namespaces/openshift-cluster-node-tuning-operator/pods/<pod-name>/logs/current.log`**
- **`cluster-scoped-resources/performance.openshift.io/performanceprofiles.yaml`** (if Performance Addon Operator)

### Cross-Component Dependencies:
- **`host_service_logs/masters/machine-config-daemon-firstboot_service.log`**
- **`host_service_logs/masters/machine-config-daemon-host_service.log`**
- **`host_service_logs/workers/machine-config-daemon-firstboot_service.log`**
- **`host_service_logs/workers/machine-config-daemon-host_service.log`**
- **`host_service_logs/masters/crio_service.log`**
- **`host_service_logs/workers/crio_service.log`**

---

## 6. Pod & Container Issues

**Keywords**: `pod`, `container`, `crash`, `restart`, `pending`, `image pull`, `pull backoff`, `container creating`, `terminating`, `evicted`, `oom`, `out of memory`, `startup probe`, `liveness probe`, `readiness probe`

### Primary Files (MANDATORY):
- **`namespaces/<namespace>/pods/<pod-name>/<container-name>/<container-name>/logs/current.log`**
- **`namespaces/<namespace>/pods/<pod-name>/<container-name>/<container-name>/logs/previous.log`**
- **`namespaces/<namespace>/pods/<pod-name>/<pod-name>.yaml`**
- **`namespaces/<namespace>/core/events.yaml`**

### Workload Controllers:
- **`namespaces/<namespace>/apps/deployments.yaml`**
- **`namespaces/<namespace>/apps/daemonsets.yaml`**
- **`namespaces/<namespace>/apps/statefulsets.yaml`**
- **`namespaces/<namespace>/core/pods.yaml`**

### Configuration:
- **`namespaces/<namespace>/core/configmaps.yaml`**
- **`namespaces/<namespace>/core/secrets.yaml`**
- **`namespaces/<namespace>/core/services.yaml`**

### Cross-Component Dependencies:
- **`host_service_logs/masters/crio_service.log`**
- **`host_service_logs/workers/crio_service.log`**
- **`host_service_logs/masters/kubelet_service.log`**
- **`host_service_logs/workers/kubelet_service.log`**

---

## 7. Performance & Resource Issues

**Keywords**: `performance`, `metrics`, `cpu`, `memory`, `resource`, `quota`, `hpa`, `autoscaling`, `slow`, `latency`, `high load`, `SystemMemoryExceedsReservation`

### Primary Files (MANDATORY):
- **`monitoring/metrics/metrics.openmetrics`** (Conditional - requires gather_metrics)
- **`monitoring/prometheus/status/config.json`**
- **`monitoring/prometheus/status/flags.json`**
- **`nodes/<node-name>/*`** (all node performance data — wildcard required, a bare `nodes/<node-name>/` does not resolve)

### For SystemMemoryExceedsReservation / kubelet reservation alerts:
**Also apply Section 27 first** — KubeletConfig / `autoSizingReserved` validation before treating monitoring as primary.

### Prometheus Data:
- **`monitoring/prometheus/<pod-name>/active-targets.json`**
- **`monitoring/prometheus/<pod-name>/status/tsdb.json`**
- **`monitoring/prometheus/<pod-name>/status/runtimeinfo.json`**
- **`monitoring/alertmanager/status.json`**

### Resource Quotas:
- **`namespaces/<namespace>/core/resourcequotas.yaml`**
- **`cluster-scoped-resources/quota.openshift.io/clusterresourcequotas.yaml`**

### Autoscaling:
- **`namespaces/<namespace>/autoscaling/horizontalpodautoscalers.yaml`**
- **`cluster-scoped-resources/autoscaling.openshift.io/clusterautoscalers.yaml`**

### Cross-Component Dependencies:
- **`namespaces/openshift-kube-apiserver/pods/<pod-name>/kube-apiserver/kube-apiserver/api_priority_and_fairness/queues`**
- **`etcd_info/object_count.json`**

---

## 8. Security & Audit Issues

**Keywords**: `audit`, `security`, `rbac`, `role`, `binding`, `service account`, `certificate`, `csr`, `scc`, `security context constraints`

### Primary Files (MANDATORY):
- **`audit_logs/kube-apiserver/<node-name>-audit.log`** (Conditional)
- **`audit_logs/openshift-apiserver/<node-name>-audit.log`** (Conditional)
- **`audit_logs/oauth-apiserver/<node-name>-audit.log`** (Conditional)

### RBAC:
- **`cluster-scoped-resources/rbac.authorization.k8s.io/clusterroles.yaml`**
- **`cluster-scoped-resources/rbac.authorization.k8s.io/clusterrolebindings.yaml`**
- **`namespaces/<namespace>/rbac.authorization.k8s.io/roles.yaml`**
- **`namespaces/<namespace>/rbac.authorization.k8s.io/rolebindings.yaml`**

### Security Context Constraints:
- **`cluster-scoped-resources/security.openshift.io/securitycontextconstraints.yaml`**

### Certificates:
- **`cluster-scoped-resources/core/certificatesigningrequests.yaml`**
- **`namespaces/openshift-service-ca/pods/<pod-name>/logs/current.log`**

---

## 9. Service Mesh & Istio Issues (Conditional - if Istio installed)

**Keywords**: `istio`, `service mesh`, `envoy`, `kiali`, `virtual service`, `destination rule`, `gateway`

> This entire section is conditional. Files only exist if Istio/Service Mesh is installed on the cluster.

### Primary Files (MANDATORY):
- **`istio/namespaces/<namespace>/pods/<pod-name>/config_dump_istiod.json`**
- **`istio/namespaces/<namespace>/pods/<pod-name>/config_dump_proxy.json`**
- **`istio/namespaces/<namespace>/pods/<pod-name>/proxy_stats`**

### Control Plane:
- **`istio/namespaces/<namespace>/<revision>/debug-syncz.json`**
- **`istio/cluster-scoped-resources/networking.istio.io/`**

---

## 10. Monitoring & Metrics Issues

**Keywords**: `prometheus`, `alertmanager`, `alert`, `metrics`, `monitoring`, `grafana`

### Primary Files (MANDATORY):
- **`monitoring/prometheus/rules.json`**
- **`monitoring/prometheus/alertmanagers.json`**
- **`monitoring/alertmanager/status.json`**
- **`namespaces/openshift-monitoring/pods/<pod-name>/logs/current.log`**
- **`namespaces/openshift-monitoring/pods/<pod-name>/logs/previous.log`**

### Metrics Collection:
- **`monitoring/metrics/metrics.openmetrics`** (Conditional - requires gather_metrics)
- **`monitoring/metrics/metrics.stderr`**

---

## 11. Windows Node Issues

**Keywords**: `windows`, `windows node`, `hybrid`, `wicd`, `containerd`

### Primary Files (MANDATORY):
- **`host_service_logs/windows/log_files/kubelet/kubelet.log`**
- **`host_service_logs/windows/log_files/containerd/containerd.log`**
- **`host_service_logs/windows/log_files/kube-proxy/kube-proxy.log`**

### Windows-Specific:
- **`host_service_logs/windows/log_files/wicd/`** (all WICD logs)
- **`host_service_logs/windows/log_files/hybrid-overlay/hybrid-overlay.log`**
- **`host_service_logs/windows/log_files/csi-proxy/csi-proxy.log`**

---

## 12. Platform-Specific Issues (vSphere, ARO, etc.)

### vSphere:
- **`namespaces/openshift-vsphere-csi-driver/pods/<pod-name>/logs/current.log`**
- **`cluster-scoped-resources/csinodetopologies.cns.vmware.com/`**

### ARO (Azure Red Hat OpenShift):
- **`namespaces/openshift-azure-operator/pods/<pod-name>/logs/current.log`**
- **`namespaces/openshift-azure-logging/pods/<pod-name>/logs/current.log`**

---

## 13. etcd Issues

**Keywords**: `etcd`, `quorum`, `member`, `alarm`, `slow`, `grpc`, `endpoint`, `database`, `corruption`, `etcdGRPCRequestsSlow`, `spike`, `performance`, `azure`, `slow requests`

### Primary Files (MANDATORY):
- **`etcd_info/endpoint_health.json`**
- **`etcd_info/endpoint_status.json`**
- **`etcd_info/member_list.json`**
- **`etcd_info/alarm_list.json`**
- **`etcd_info/object_count.json`**

### etcd Logs:
(MANDATORY: include both current.log and previous.log, and core/events.yaml.)
- **`audit_logs/etcd/<node-name>-audit.log`** (Conditional)
- **`namespaces/openshift-etcd/pods/<pod-name>/<container-name>/<container-name>/logs/current.log`**
- **`namespaces/openshift-etcd/pods/<pod-name>/<container-name>/<container-name>/logs/previous.log`**
- **`namespaces/openshift-etcd/core/events.yaml`**

### etcd Operator:
(MANDATORY: include both current.log and previous.log, and core/events.yaml.)
- **`namespaces/openshift-etcd-operator/pods/<pod-name>/<container-name>/<container-name>/logs/current.log`**
- **`namespaces/openshift-etcd-operator/pods/<pod-name>/<container-name>/<container-name>/logs/previous.log`**
- **`namespaces/openshift-etcd-operator/core/events.yaml`**

### Cross-Component Dependencies (MANDATORY for etcd issues):
Include all files from **Section 1 (API Server)** — specifically:
- **`namespaces/openshift-kube-apiserver/pods/<pod-name>/<container-name>/<container-name>/logs/current.log`** and **`previous.log`**
- **`namespaces/openshift-kube-apiserver/pods/<pod-name>/kube-apiserver/kube-apiserver/api_priority_and_fairness/queues`**
- **`static-pods/kube-apiserver/<node-name>-startup.log.gz`** (compressed)
- **`static-pods/kube-apiserver/<node-name>-termination.log.gz`** (compressed)
- **`audit_logs/kube-apiserver/<node-name>-audit.log`** (Conditional)

Plus:
- **`monitoring/metrics/metrics.openmetrics`** (Conditional - requires gather_metrics)
- **`host_service_logs/masters/kubelet_service.log`**
- **`cluster-scoped-resources/config.openshift.io/clusteroperators.yaml`**
- **`cluster-scoped-resources/config.openshift.io/infrastructures.yaml`**
- **`nodes/<node-name>/*`**

**For etcd slow/GRPC or performance spike** (e.g. etcdGRPCRequestsSlow spike on Azure CI): also include **`monitoring/metrics/metrics.openmetrics`** and **`nodes/*/*`** for CPU/load correlation.

---

## 14. Storage Version Migration Issues

**Keywords**: `storage version migration`, `kube-storage-version-migrator`, `api version`, `migration`, `deploying`, `available false`, `KubeStorageVersionMigrator_Deploying`, `updates`, `upgrade`, `Available=False`

### Primary Files (MANDATORY):
(MANDATORY: list both current.log and previous.log as two separate lines in your output.)
- **`cluster-scoped-resources/migration.k8s.io/storageversionmigrations.yaml`**
- **`namespaces/openshift-kube-storage-version-migrator/pods/<pod-name>/logs/current.log`**
- **`namespaces/openshift-kube-storage-version-migrator/pods/<pod-name>/logs/previous.log`**
- **`namespaces/openshift-kube-storage-version-migrator/core/events.yaml`**

### Migration Resources:
- **`namespaces/openshift-kube-storage-version-migrator/apps/deployments.yaml`**
- **`namespaces/openshift-kube-storage-version-migrator/batch/jobs.yaml`**
- **`namespaces/openshift-kube-storage-version-migrator/core/configmaps.yaml`**

### API Resources:
- **`cluster-scoped-resources/apiregistration.k8s.io/apiservices.yaml`**
- **`cluster-scoped-resources/apiextensions.k8s.io/customresourcedefinitions.yaml`**
- **`cluster-scoped-resources/storage.k8s.io/storageclasses.yaml`**

### Cross-Component Dependencies (MANDATORY for storage migration issues):
- **`cluster-scoped-resources/config.openshift.io/clusteroperators.yaml`**
- **`namespaces/openshift-cluster-version/core/events.yaml`**
- **`namespaces/openshift-cluster-version/pods/<pod-name>/logs/current.log`**
- **`namespaces/openshift-cluster-version/pods/<pod-name>/logs/previous.log`**
- **`audit_logs/kube-apiserver/<node-name>-audit.log`**
- **`audit_logs/openshift-apiserver/<node-name>-audit.log`**
- **`namespaces/openshift-kube-apiserver/pods/<pod-name>/logs/current.log`**
- **`namespaces/openshift-kube-apiserver/pods/<pod-name>/logs/previous.log`**
- **`namespaces/openshift-kube-apiserver/core/events.yaml`**
- **`static-pods/kube-apiserver/<node-name>-startup.log.gz`** (compressed)
- **`static-pods/kube-apiserver/<node-name>-termination.log.gz`** (compressed)
- **`etcd_info/endpoint_health.json`**
- **`etcd_info/endpoint_status.json`**
- **`etcd_info/member_list.json`**
- **`etcd_info/alarm_list.json`**
- **`etcd_info/object_count.json`**

---

## 15. IPsec & Network Security Issues

**Keywords**: `ipsec`, `encryption`, `libreswan`, `xfrm`, `traffic status`, `network security`, `tunnel`, `sig-network`, `Feature:IPsec`, `traffic with IPsec`, `ovn-kubernetes check traffic`

### Primary Files (MANDATORY):
- **`network_logs/ipsec/status/`** (all status files)
- **`network_logs/ipsec/trafficstatus/`** (all traffic status files)
- **`network_logs/ipsec/xfrm/`** (all XFRM state and policy files)

### IPsec Configuration:
- **`network_logs/ipsec/<pod-name>_ipsec.conf`** (all pod configurations)
- **`network_logs/ipsec/<pod-name>_ipsec.d/`** (all configuration directories)
- **`network_logs/ipsec/<pod-name>_libreswan.log`** (all Libreswan logs)

### Network Connectivity Validation:
- **`pod_network_connectivity_check/podnetworkconnectivitychecks.yaml`**

**For IPsec + OVN traffic checks** (e.g. sig-network Feature:IPsec, "check traffic with IPsec"): include **`network_logs/ipsec/trafficstatus/`**, **`network_logs/ipsec/status/`**, and OVN pod logs/events below.

### Cross-Component Dependencies (MANDATORY for IPsec issues):
- **`network_logs/leader_ovnnb_status`**
- **`network_logs/leader_ovnsb_status`**
- **`network_logs/ovn_kubernetes_top_pods`**
- **`network_logs/cluster_scale`**
- **`namespaces/openshift-ovn-kubernetes/pods/<pod-name>/logs/current.log`**
- **`namespaces/openshift-ovn-kubernetes/pods/<pod-name>/logs/previous.log`**
- **`namespaces/openshift-ovn-kubernetes/core/events.yaml`**
- **`namespaces/openshift-network-operator/pods/<pod-name>/logs/current.log`**
- **`namespaces/openshift-network-operator/pods/<pod-name>/logs/previous.log`**
- **`namespaces/openshift-network-operator/core/events.yaml`**
- **`host_service_logs/masters/NetworkManager_service.log`**
- **`host_service_logs/workers/NetworkManager_service.log`**
- **`host_service_logs/masters/crio_service.log`**
- **`host_service_logs/workers/crio_service.log`**
- **`cluster-scoped-resources/config.openshift.io/networks.yaml`**

---

## 16. External DNS / API Resolution (infrastructure)

**Keywords**: `external DNS`, `DNS record`, `api-int`, `api.<domain>`, `*.apps`, `no such host`, `NXDOMAIN`, `lookup failure`, `VIP DNS`, `load balancer DNS`, `NotReady master`, `API unreachable`, `RHOSO`, `Nova down`

### Primary Files (MANDATORY — HIGH):
- **`cluster-scoped-resources/config.openshift.io/infrastructures.yaml`**
- **`cluster-scoped-resources/config.openshift.io/dnses.yaml`**
- **`pod_network_connectivity_check/podnetworkconnectivitychecks.yaml`**
- **`host_service_logs/masters/kubelet_service.log`**
- **`host_service_logs/masters/NetworkManager_service.log`**
- **`namespaces/openshift-dns/pods/*/*/*/logs/current.log`**
- **`namespaces/openshift-dns/pods/*/*/*/logs/previous.log`**
- **`namespaces/openshift-dns/core/events.yaml`**
- **`cluster-scoped-resources/config.openshift.io/clusteroperators.yaml`**

### Secondary (after L0 DNS/API checked):
- etcd health (`etcd_info/`), API server logs, OVN status — treat as cascade unless independently primary

### Outside must-gather (call out in RCA if evidence insufficient):
Verify corporate/external DNS has A/AAAA (or CNAME) records for `api`, `api-int`, and `*.apps` matching `infrastructures.yaml`. Must-gather cannot create missing external records; if lookup failures dominate, state this explicitly.

---

## 17. Enterprise Proxy / Image Pull / TLS Trust

**Keywords**: `proxy`, `x509`, `certificate signed by unknown authority`, `ImagePullBackOff`, `ErrImagePull`, `additionalTrustBundle`, `TLS inspection`, `MITM`, `HTTPS_PROXY`

### Primary Files (MANDATORY — HIGH):
- **`cluster-scoped-resources/config.openshift.io/proxies.yaml`**
- **`cluster-scoped-resources/config.openshift.io/images.yaml`**
- **`host_service_logs/masters/kubelet_service.log`**
- **`host_service_logs/masters/crio_service.log`**
- **`host_service_logs/workers/kubelet_service.log`**
- **`host_service_logs/workers/crio_service.log`**
- **`namespaces/openshift-image-registry/pods/<pod-name>/logs/current.log`**
- **`namespaces/openshift-image-registry/pods/<pod-name>/logs/previous.log`**
- **`namespaces/openshift-image-registry/core/events.yaml`**
- Affected namespace **`core/events.yaml`** for ImagePullBackOff details

---

## 18. Machine API / Node Provisioning

**Keywords**: `machine api`, `machineset`, `machine`, `MachineHealthCheck`, `node not joining`, `provision`, `bootstrap machine`, `bare metal`, `BMH`

### Primary Files (MANDATORY):
- **`namespaces/openshift-machine-api/core/events.yaml`**
- **`namespaces/openshift-machine-api/pods/<pod-name>/logs/current.log`**
- **`namespaces/openshift-machine-api/pods/<pod-name>/logs/previous.log`**
- **`namespaces/openshift-machine-api/apps/deployments.yaml`** (operator deployment status)
- **`cluster-scoped-resources/machine.openshift.io/machines/`** (individual Machine CRs with providerStatus/conditions)
- **`cluster-scoped-resources/machine.openshift.io/machinesets/`** (desired vs current replica counts)
- **`cluster-scoped-resources/machine.openshift.io/machinehealthchecks/`** (if MHC-related)
- **`cluster-scoped-resources/core/nodes/*.yaml`**
- **`cluster-scoped-resources/config.openshift.io/infrastructures.yaml`**
- **`host_service_logs/masters/kubelet_service.log`** / **`workers/kubelet_service.log`**
- Machine Config Operator files from **Section 5** when MCO is also degraded

---

## 19. Image Registry Issues

**Keywords**: `image pull`, `registry`, `ImagePullBackOff`, `image`, `registry unavailable`, `imagestream`

### Primary Files (MANDATORY):
- **`cluster-scoped-resources/config.openshift.io/images.yaml`**
- **`cluster-scoped-resources/config.openshift.io/proxies.yaml`**
- **`namespaces/openshift-image-registry/pods/<pod-name>/logs/current.log`**
- **`namespaces/openshift-image-registry/pods/<pod-name>/logs/previous.log`**
- **`namespaces/openshift-image-registry/core/events.yaml`**
- **`namespaces/<namespace>/core/events.yaml`**
- **`host_service_logs/masters/crio_service.log`** / **`workers/crio_service.log`**

---

## 20. Ingress / Routes

**Keywords**: `ingress`, `route`, `haproxy`, `apps URL`, `*.apps`, `router`, `HTTP 503 route`

### Primary Files (MANDATORY):
- **`ingress_controllers/default/<pod-name>/haproxy.config`**
- **`namespaces/openshift-ingress/pods/<pod-name>/logs/current.log`**
- **`namespaces/openshift-ingress/pods/<pod-name>/logs/previous.log`**
- **`namespaces/openshift-ingress/core/events.yaml`**
- **`namespaces/openshift-ingress/apps/deployments.yaml`** (router deployment status)
- **`namespaces/openshift-ingress-operator/pods/<pod-name>/logs/current.log`**
- **`namespaces/openshift-ingress-operator/pods/<pod-name>/logs/previous.log`**
- **`namespaces/openshift-ingress-operator/core/events.yaml`**
- **`namespaces/<namespace>/route.openshift.io/routes.yaml`**
- **`namespaces/<namespace>/core/services.yaml`** (backend service for the route)
- **`cluster-scoped-resources/config.openshift.io/infrastructures.yaml`**
- **`cluster-scoped-resources/config.openshift.io/dnses.yaml`** (*.apps external DNS)

Do **not** default to OVN-only when the symptom is route/apps URL failure.

---

## 21. Cluster Upgrade / CVO

**Keywords**: `upgrade`, `update`, `CVO`, `cluster version`, `stuck upgrade`, `Progressing`, `Upgradeable=False`

### Primary Files (MANDATORY):
- **`cluster-scoped-resources/config.openshift.io/clusterversions.yaml`** (or `clusterversions/`)
- **`cluster-scoped-resources/config.openshift.io/clusteroperators.yaml`**
- **`cluster-scoped-resources/config.openshift.io/featuregates.yaml`** (feature gates can block upgrades)
- **`namespaces/openshift-cluster-version/core/events.yaml`**
- **`namespaces/openshift-cluster-version/pods/<pod-name>/logs/current.log`**
- **`namespaces/openshift-cluster-version/pods/<pod-name>/logs/previous.log`**
- Degraded operator namespace events + pod logs
- **`cluster-scoped-resources/machineconfiguration.openshift.io/machineconfigpools.yaml`** when MCP/drain blocks upgrade
- **`namespaces/openshift-machine-config-operator/pods/<pod-name>/logs/current.log`** and **`previous.log`**, **`core/events.yaml`** (MCO commonly blocks upgrades)

---

## 22. Workloads (Deployments / Jobs)

**Keywords**: `deployment`, `rollout`, `replica`, `statefulset`, `daemonset`, `job`, `cronjob`, `CrashLoopBackOff` (app workload)

### Primary Files (MANDATORY):
- **`namespaces/<namespace>/apps/deployments.yaml`**, **`replicasets.yaml`**, **`statefulsets.yaml`**, **`daemonsets.yaml`** as relevant
- **`namespaces/<namespace>/batch/jobs.yaml`**, **`cronjobs.yaml`** when job-related
- **`namespaces/<namespace>/core/events.yaml`**, **`core/pods.yaml`**
- Failing pod **`current.log`** and **`previous.log`**

---

## 23. Scheduler / Controller Manager

**Keywords**: `FailedScheduling`, `Pending`, `scheduler`, `controller-manager`, `replicas not created`

### Primary Files (MANDATORY):
- **`namespaces/openshift-kube-scheduler/pods/<pod-name>/logs/current.log`** and **`previous.log`**
- **`namespaces/openshift-kube-scheduler/core/events.yaml`**
- **`cluster-scoped-resources/config.openshift.io/schedulers.yaml`** (if present)
- **`cluster-scoped-resources/core/nodes/*.yaml`**
- **`namespaces/<namespace>/core/events.yaml`**
- **`namespaces/openshift-kube-controller-manager/pods/<pod-name>/logs/current.log`** and **`previous.log`** when controllers stuck

---

## 24. Admission Webhooks

**Keywords**: `admission`, `validating webhook`, `mutating webhook`, `webhook timeout`, `denied by webhook`, `MutatingAdmissionWebhook`, `ValidatingAdmissionWebhook`, `failed to complete mutation`, `timeoutSeconds`, `failurePolicy`

### Primary Files (MANDATORY — HIGH):
- **`cluster-scoped-resources/admissionregistration.k8s.io/mutatingwebhookconfigurations/`** (ALL objects)
- **`cluster-scoped-resources/admissionregistration.k8s.io/validatingwebhookconfigurations/`** (ALL objects)
- Or aggregated YAML under `admissionregistration.k8s.io/` if that is how must-gather stored them
- **Endpoints / EndpointSlices** for each webhook `clientConfig.service` namespace
- Webhook operator/injector **pod logs** (`current.log` + `previous.log`) and **`core/events.yaml`** in each webhook namespace identified from the CRs
- **`audit_logs/kube-apiserver/`** (Conditional) and apiserver pod logs — supporting dial/timeout evidence only

### Mandatory analysis procedure (do not skip):
1. **Inventory every** MutatingWebhookConfiguration and ValidatingWebhookConfiguration — not a sample from apiserver log lines.
2. For each entry record: **name**, **service namespace/name/port**, **`timeoutSeconds`**, **`failurePolicy`**, **endpoint count** (0 = dead backend).
3. **Literal timeout match:** If the user error says `in Ns` / `N seconds` / `timeout … N`, flag every webhook whose `timeoutSeconds` equals **N** (exact match is critical — e.g. error "in 13s" ↔ `timeoutSeconds: 13`). Also note webhooks whose timeouts sum toward the admission budget.
4. Common third-party injectors often appear (Vault agent injector, Dynatrace, OpenTelemetry/`mpod`, DevWorkspace, CloudBees, Contrast, StackRox/ACS, service-mesh sidecars). **Discover them from the CR list** — never assume finding Dynatrace/OTel alone is complete if Vault or others are also present.
5. **Causal ranking:** Unreachable/slow webhooks with `failurePolicy: Fail` (or cumulative timeouts exhausting the admission window) are the **primary actionable cause** for "MutatingAdmissionWebhook failed to complete mutation" unless the inventory shows all webhooks healthy.
6. **Remediation preference:** remove, disable, raise timeout, or set `failurePolicy: Ignore` on the failing webhook(s); verify endpoints/pods. Do **not** lead with kube-apiserver CrashLoopBackOff / OVN / RBAC rebuild as the primary fix when webhook inventory explains the error.
7. Control-plane/OVN/RBAC noise may be concurrent or secondary — document under Secondary Causes unless webhooks are proven healthy and timeouts persist.

---

## 25. RHOSO / OpenStack on OpenShift

**Keywords**: `RHOSO`, `OpenStack`, `Nova`, `Neutron`, `Keystone`, `Galera`, `RabbitMQ`, `Heat`, `Cinder`, `Horizon`, `openstack namespace`

### Primary Files (MANDATORY):
1. Apply **Section 16** first if masters NotReady / API unreachable (Nova-down is often cascade)
2. **`namespaces/openstack/core/events.yaml`**
3. **`namespaces/openstack/pods/<pod-name>/logs/current.log`** and **`previous.log`** for affected services
4. **`cluster-scoped-resources/config.openshift.io/clusteroperators.yaml`**
5. **`infrastructures.yaml`**, **`dnses.yaml`**, **`proxies.yaml`**, **`images.yaml`**

---

## 26. Insights / Compliance

**Keywords**: `insights`, `compliance`, `insights-operator`

### Primary Files (MANDATORY):
- **`insights-data/`**
- **`namespaces/openshift-insights/pods/<pod-name>/logs/current.log`** and **`previous.log`**
- **`namespaces/openshift-insights/core/events.yaml`**

---

## 27. KubeletConfig / SystemMemoryExceedsReservation

**Keywords**: `SystemMemoryExceedsReservation`, `autoSizingReserved`, `KubeletConfig`, `systemReserved`, `kubeReserved`, `auto-sizing`, `memory reservation`, `allocatable memory`

### Primary Files (MANDATORY — HIGH, before monitoring):
- **`cluster-scoped-resources/machineconfiguration.openshift.io/kubeletconfigs/`** (or `kubeletconfigs.yaml`)
- **`cluster-scoped-resources/machineconfiguration.openshift.io/machineconfigs.yaml`** (incl. `*auto-sizing*` MachineConfigs)
- **`cluster-scoped-resources/machineconfiguration.openshift.io/machineconfigpools.yaml`**
- **`host_service_logs/masters/kubelet_service.log`** / **`workers/kubelet_service.log`**
- **`cluster-scoped-resources/core/nodes/*.yaml`** (capacity vs allocatable)
- **`machine_config_ondisk/<node-name>/mcs-machine-config-content.json`** when present (rendered kubelet config)

### Field-placement rules (CRITICAL — common misconfig):
- **`autoSizingReserved`** must be at **`spec.autoSizingReserved`** (boolean on the KubeletConfig CR).
- It must **NOT** be nested under **`spec.kubeletConfig`** (or other wrong parents). Wrong placement is silently ignored → reservations stay wrong → `SystemMemoryExceedsReservation` fires.
- Do **not** infer root cause from MachineConfig filenames like `50-*-auto-sizing-disabled.yaml` alone — always open the KubeletConfig YAML and verify field paths.
- **`systemReserved` / `kubeReserved`** live under **`spec.kubeletConfig`** when statically set; confirm they match intent when auto-sizing is off.

### Secondary only after KubeletConfig is correct:
- Monitoring stack (`monitoring/prometheus/`, cAdvisor) — metric noise is not primary if `autoSizingReserved` is misplaced
- Workload pressure / OOM — possible contributors, not substitutes for fixing CR placement
- Upgrade/MCO churn — may amplify symptoms but does not replace config validation

### Remediation hint:
If `autoSizingReserved` is under the wrong key, the fix is to move it to `spec.autoSizingReserved` and let MCO/kubelet reconcile — not to resize workloads or rebuild Prometheus first.

---

## 28. OLM / OperatorHub / Subscriptions

**Keywords**: `OLM`, `OperatorHub`, `Subscription`, `CatalogSource`, `InstallPlan`, `CSV`, `ClusterServiceVersion`, `operator install`, `operator upgrade`, `marketplace`, `catalogd`

### Primary Files (MANDATORY):
- **`namespaces/openshift-operator-lifecycle-manager/pods/<pod-name>/logs/current.log`** and **`previous.log`**
- **`namespaces/openshift-operator-lifecycle-manager/core/events.yaml`**
- **`namespaces/openshift-marketplace/pods/<pod-name>/logs/current.log`** and **`previous.log`** (CatalogSource pods)
- **`namespaces/openshift-marketplace/core/events.yaml`**

### Operator-Specific (when target operator namespace known):
- **`namespaces/<operator-namespace>/operators.coreos.com/subscriptions.yaml`**
- **`namespaces/<operator-namespace>/operators.coreos.com/installplans.yaml`**
- **`namespaces/<operator-namespace>/operators.coreos.com/clusterserviceversions.yaml`**
- **`cluster-scoped-resources/apiextensions.k8s.io/customresourcedefinitions/`** (CRDs installed by the operator)

### Cross-Component Dependencies:
- **`cluster-scoped-resources/config.openshift.io/clusteroperators.yaml`** (marketplace operator status)
- **`namespaces/openshift-catalogd/pods/<pod-name>/logs/current.log`** (if catalogd-based OLM)

---

## 29. Console / FeatureGate

**Keywords**: `console`, `web console`, `FeatureGate`, `TechPreview`, `TechPreviewNoUpgrade`, `feature gate`, `console URL`, `console login`

### Primary Files (MANDATORY):
- **`cluster-scoped-resources/config.openshift.io/consoles.yaml`** (console URL, OAuth redirect config)
- **`cluster-scoped-resources/config.openshift.io/featuregates.yaml`** (enabled feature sets, TechPreviewNoUpgrade)
- **`namespaces/openshift-console/pods/<pod-name>/logs/current.log`** and **`previous.log`**
- **`namespaces/openshift-console/core/events.yaml`**
- **`namespaces/openshift-console-operator/pods/<pod-name>/logs/current.log`** and **`previous.log`**
- **`namespaces/openshift-console-operator/core/events.yaml`**

### Cross-Component Dependencies:
- **`cluster-scoped-resources/config.openshift.io/authentications.yaml`** (console login depends on OAuth)
- **`cluster-scoped-resources/config.openshift.io/infrastructures.yaml`** and **`dnses.yaml`** (console route DNS)
- Ingress files from **Section 20** when console route itself is unreachable

---

## Cross-Component Analysis Rules

### When loss of APIServer networking + etcd quorum + high CPU (mass test failure):
**Include all of**: API server (category 1), etcd (category 13), networking/OVN (category 3), plus metrics and node data:
- **API server**: `namespaces/openshift-kube-apiserver/` (events, pods/*/logs/current.log and previous.log), `audit_logs/kube-apiserver/`, `static-pods/kube-apiserver/`, `api_priority_and_fairness/queues`
- **etcd**: All `etcd_info/*.json`, `namespaces/openshift-etcd/` and `openshift-etcd-operator/` (events, pods/*/logs/current and previous)
- **Networking**: `pod_network_connectivity_check/podnetworkconnectivitychecks.yaml`, `network_logs/` (cluster_scale, plus leader_ovnnb_status/leader_ovnsb_status **only if legacy OVN mode**), `namespaces/openshift-ovn-kubernetes/` (events, pods/*/logs/current and previous)
- **CPU/load**: `monitoring/metrics/metrics.openmetrics`, `nodes/*/*`, `host_service_logs/masters/kubelet_service.log`
- **Cluster status**: `cluster-scoped-resources/config.openshift.io/clusteroperators.yaml`

### When etcd issues are suspected:
**ALWAYS include API server components** (categories 1 + 13):
- All etcd files from category 13
- All API server files from category 1
- Performance monitoring from category 7

### When networking issues are suspected:
**ALWAYS include DNS/API resolution first** (categories 3 + 16), then CNI if still needed:
- Section 16 primary files (infrastructures, dnses, connectivity checks, kubelet)
- Networking files from category 3
- Container runtime logs (`host_service_logs/*/crio_service.log`) only when runtime/CNI is implicated — not as the default primary for every network symptom
- Pod logs if specific pods are affected

### When masters are NotReady / API unreachable:
**ALWAYS include Section 16 before OVN/etcd deep-dives**:
- infrastructures.yaml, dnses.yaml, podnetworkconnectivitychecks, kubelet_service.log
- Then etcd + API server if DNS/API resolution is ruled out or confirmed secondary

### When x509 / ImagePull / external registry failures are present:
**ALWAYS include Section 17** (proxies.yaml, images.yaml, kubelet/crio) before blaming only CRI-O runtime bugs

### When SystemMemoryExceedsReservation / kubelet reservation alerts are present:
**ALWAYS include Section 27 first** (KubeletConfig CRs + `autoSizingReserved` placement check). Do **not** promote Prometheus/cAdvisor/TLS monitoring errors as primary until KubeletConfig field placement is validated.

### When MutatingAdmissionWebhook / ValidatingAdmissionWebhook timeout or "failed to complete mutation" errors are present:
**ALWAYS include Section 24 first** — full webhook CR inventory, `timeoutSeconds` literal match to the error, and endpoint health. Do **not** promote kube-apiserver CrashLoop / OVN / RBAC cascade as primary until the webhook inventory is complete.

### When storage issues are suspected:
**ALWAYS include node and kubelet logs** (categories 4 + 5):
- All storage files from category 4
- Node kubelet logs: `host_service_logs/*/kubelet_service.log`
- Node status: `cluster-scoped-resources/core/nodes/<node-name>.yaml`

### When operator issues are suspected:
**ALWAYS include cluster version and events** (category 2):
- Operator-specific namespace logs
- `cluster-scoped-resources/config.openshift.io/clusteroperators.yaml`
- `namespaces/openshift-cluster-version/core/events.yaml`
- For OLM-managed operators: also apply **Section 28** (OLM Subscriptions, CatalogSources, InstallPlans)

### When console access or FeatureGate issues are suspected:
**ALWAYS include Section 29** (consoles.yaml, featuregates.yaml, console/console-operator pods). For upgrades blocked by FeatureGate, also include Section 21 (Upgrade/CVO).

---

## File Priority Rules

### High Priority (always include first):
1. **Infrastructure prerequisites** when symptoms match: `infrastructures.yaml`, `dnses.yaml`, `proxies.yaml`, `images.yaml`
2. **Current and previous logs** for affected components
3. **Events files** for affected namespaces
4. **Cluster operator status** for operator-related issues
5. **Health/status JSON files** for infrastructure components
6. **Connectivity checks** for API/DNS/NotReady symptoms

### Medium Priority (include for context):
1. **Configuration files** (YAML resources)
2. **Cross-component logs** based on dependencies above (including OVN/CRI-O when CNI/runtime implicated)
3. **Audit logs** for API-related issues

### Low Priority (include if space permits):
1. **Metrics and monitoring data**
2. **Static pod startup/termination logs**
3. **Host service logs** for non-primary services (do not demote kubelet when NotReady/API symptoms exist — kubelet stays HIGH)

---

## Mandatory File Combinations

### For any pod issue:
- **BOTH** `logs/current.log` AND `logs/previous.log`
- **BOTH** pod YAML AND namespace events

### For any operator issue:
- **BOTH** operator pod logs AND cluster operator status
- **BOTH** current AND previous logs for operator pods

### For any API server issue:
- **BOTH** API server logs AND etcd health status
- **BOTH** audit logs AND API priority/fairness data
- **ALSO** infrastructures.yaml + dnses.yaml + connectivity checks when unreachable/timeout/NotReady

### For any networking issue:
- **BOTH** DNS/API resolution files (`infrastructures.yaml`, `dnses.yaml`, connectivity checks) AND CNI/OVN when CNI is implicated
- Prefer infrastructures + dnses as HIGH when api/api-int lookup or NotReady-master symptoms exist
- Do **not** require OVN DB + CRI-O as the only mandatory HIGH set for every networking symptom

### For any etcd issue:
- **ALL** etcd health files (endpoint_health.json, member_list.json, alarm_list.json)
- **BOTH** etcd logs AND API server logs (etcd issues always affect API server)
- Include infrastructures.yaml / dnses.yaml when peer dial / network path failures are present
