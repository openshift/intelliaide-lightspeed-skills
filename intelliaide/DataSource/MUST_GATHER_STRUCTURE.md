---
# OpenShift Must-Gather Log Structure Summary

## Overview
The OpenShift must-gather tool collects comprehensive diagnostic information from an OpenShift cluster. The **user supplies the root folder**. Under that root there is **one folder with any name** (e.g. `quay-content`—the name is not fixed). Under that folder are `host_service_logs/`, `namespaces/`, `cluster-scoped-resources/`, etc. The main `gather` script orchestrates multiple collection scripts that run in parallel to gather different types of cluster data.

## Base Directory Structure

- **`<must-gather-root>/`** — The path the **user supplies** (root folder;).
- **`<must-gather-root>/<content-folder>/`** — One child folder under the root; **name can be any string** (e.g. `quay-content`). This folder contains `version`, `audit_logs/`, `host_service_logs/`, `namespaces/`, etc.

## Path Pattern Conventions

- **Specific paths**: Use exact file names when files are always present (e.g., `version`, `endpoint_health.json`)
- **Wildcard patterns**: Use `<variable>` for dynamic components that must be substituted:
  - `<node-name>` - Actual node hostname (e.g., `ip-10-0-122-129.us-east-2.compute.internal`)
  - `<pod-name>` - Actual pod name (e.g., `etcd-ip-10-0-122-129`)
  - `<namespace>` - Actual namespace name (e.g., `openshift-etcd`)
  - `<service-name>` - Actual service name (e.g., `kubelet`, `crio`, `NetworkManager`)
- **Multiple files**: Use `*` only when multiple files of same type exist and all should be analyzed

---

## Directory Structure and Purpose

All paths below are under **`<must-gather-root>/<content-folder>/`**. The tool resolves the content folder automatically (single child under user root).

### 1. **`audit_logs/`** (Conditional)
**Purpose**: Contains API server audit logs from master nodes. Present only when audit logging is enabled and audit log collection succeeds.

**Subdirectories and Files**:
- **`kube-apiserver/`** (Always Present)
  - `<node-name>-audit.log` - Kubernetes API server audit logs per master node
  - **Priority**: Critical for API authentication, authorization, and request failures
  
- **`openshift-apiserver/`** (Always Present)
  - `<node-name>-audit.log` - OpenShift API server audit logs per master node
  - **Priority**: Critical for OpenShift-specific resource access issues
  
- **`oauth-apiserver/`** (Always Present)
  - `<node-name>-audit.log` - OAuth API server audit logs per master node
  - **Priority**: Critical for authentication and token issues
  
- **`oauth-server/`** (Always Present)
  - `<node-name>-audit.log` - OAuth server authentication logs per master node
  - **Priority**: Critical for user authentication flow problems
  
- **`etcd/`** (Always Present)
  - `<node-name>-audit.log` - etcd audit logs per master node
  - **Priority**: Critical for etcd access and cluster state issues
  
- **`monitoring/`** (Conditional - if monitoring pods exist)
  - `<pod-name>-audit.log` - Audit logs from prometheus-adapter or metrics-server pods

**Collection Script**: `gather_audit_logs`

---

### 2. **`host_service_logs/`** (Always Present)
**Purpose**: System service logs from cluster nodes

**Subdirectories and Files**:
- **`masters/`** (Always Present)
  - `kubelet_service.log` - Kubelet service logs from master nodes
  - `crio_service.log` - CRI-O container runtime logs from master nodes
  - `machine-config-daemon-firstboot_service.log` - MCO first boot logs from master nodes
  - `machine-config-daemon-host_service.log` - MCO host service logs from master nodes
  - `NetworkManager_service.log` - NetworkManager service logs from master nodes
  - `openvswitch_service.log` - Open vSwitch service logs from master nodes
  - `ovs-configuration_service.log` - OVS configuration service logs from master nodes
  - `ovs-vswitchd_service.log` - OVS daemon logs from master nodes
  - `ovsdb-server_service.log` - OVS database server logs from master nodes
  - `ostree-finalize-staged_service.log` - OSTree finalization logs from master nodes
  - `rpm-ostreed_service.log` - RPM-OSTree daemon logs from master nodes
  - **Priority**: Critical for node-level service failures and container runtime issues

- **`workers/`** (Always Present)
  - `kubelet_service.log` - Kubelet service logs from worker nodes
  - `crio_service.log` - CRI-O container runtime logs from worker nodes
  - `machine-config-daemon-firstboot_service.log` - MCO first boot logs from worker nodes
  - `machine-config-daemon-host_service.log` - MCO host service logs from worker nodes
  - `NetworkManager_service.log` - NetworkManager service logs from worker nodes
  - `openvswitch_service.log` - Open vSwitch service logs from worker nodes
  - `ovs-configuration_service.log` - OVS configuration service logs from worker nodes
  - `ovs-vswitchd_service.log` - OVS daemon logs from worker nodes
  - `ovsdb-server_service.log` - OVS database server logs from worker nodes
  - `ostree-finalize-staged_service.log` - OSTree finalization logs from worker nodes
  - `rpm-ostreed_service.log` - RPM-OSTree daemon logs from worker nodes
  - **Priority**: Critical for node-level service failures and container runtime issues

- **`windows/`** (Conditional - if Windows nodes exist)
  - `log_files/kube-proxy/kube-proxy.log` - Windows kube-proxy logs
  - `log_files/hybrid-overlay/hybrid-overlay.log` - Windows hybrid overlay logs
  - `log_files/kubelet/kubelet.log` - Windows kubelet logs
  - `log_files/containerd/containerd.log` - Windows containerd logs
  - `log_files/wicd/` - Windows Instance Config Daemon logs
  - `log_files/csi-proxy/csi-proxy.log` - Windows CSI proxy logs

**Collection Scripts**: `gather_service_logs`, `gather_windows_node_logs`

---

### 3. **`monitoring/`** (Conditional - requires monitoring pods)
**Purpose**: Prometheus and Alertmanager monitoring data. Present only when monitoring stack pods are running.

**Subdirectories and Files**:
- **`prometheus/`** (Always Present)
  - `alertmanagers.json` - Alertmanager configuration and discovery
  - `rules.json` - All Prometheus recording and alerting rules
  - `status/config.json` - Current Prometheus configuration
  - `status/flags.json` - Prometheus startup flags and settings
  - `<pod-name>/active-targets.json` - Active scrape targets per Prometheus replica
  - `<pod-name>/status/runtimeinfo.json` - Runtime information per Prometheus replica
  - `<pod-name>/status/tsdb.json` - Time-series database status per Prometheus replica
  - **Priority**: Critical for monitoring stack issues and performance analysis

- **`alertmanager/`** (Always Present)
  - `status.json` - Alertmanager status and configuration
  - `status.stderr` - Alertmanager status collection errors
  - **Priority**: Critical for alerting and notification issues

- **`metrics/`** (Always Present)
  - `metrics.openmetrics` - Complete metrics dump in OpenMetrics format
  - `metrics.stderr` - Metrics collection errors
  - **Priority**: Critical for performance analysis and resource usage investigation

**Collection Scripts**: `gather_monitoring`, `gather_metrics`

---

### 4. **`insights-data/`** (Always Present)
**Purpose**: Insights Operator archive data

**Contents**: Complete copy of `/var/lib/insights-operator` from the insights operator pod, containing:
- Cluster configuration snapshots
- Health check results
- Performance data
- Compliance information
- **Priority**: Medium for compliance and configuration analysis

**Collection Script**: `gather_insights`

---

### 5. **`etcd_info/`** (Always Present)
**Purpose**: etcd cluster information and diagnostics

**Files**:
- `member_list.json` - etcd cluster member list and status
- `endpoint_status.json` - Detailed status of all etcd endpoints
- `endpoint_health.json` - Health status of all etcd endpoints
- `alarm_list.json` - List of active etcd alarms and warnings
- `object_count.json` - Count of Kubernetes objects by type in etcd
- **Priority**: Critical for etcd cluster health, quorum issues, and performance problems

**Collection Script**: `gather_etcd`

---

### 6. **`network_logs/`** (Always Present)
**Purpose**: Network-related logs and configurations

**Subdirectories and Files**:
- **`ovnk_database_store.tar.gz`** (Conditional - if OVN-Kubernetes is used)
  - Compressed archive containing OVN Northbound and Southbound database files. In **interconnect mode** (multi-zone, the current default topology) this contains one NB/SB DB pair **per node/pod** (`<ovnkube-node-pod>_nbdb`, `<ovnkube-node-pod>_sbdb`); in **legacy (single-zone) mode** it is not produced this way — see `leader_nbdb`/`leader_sbdb` below instead
  - **Priority**: Critical for OVN network state analysis and logical topology issues

- **`ovnk_extras_store.tar.gz`** (Conditional - **interconnect mode only**)
  - Compressed archive of extra `ovnkube-controller` logs (`libovsdb*.log`) collected per `ovnkube-node` pod. Does not exist in legacy (single-zone) OVN mode.
  - **Priority**: Medium for OVN libovsdb-level debugging in interconnect-mode clusters

- **`ipsec/`** (Conditional - if IPsec is enabled)
  - `xfrm/` - IPsec XFRM state and policy information
  - `status/` - IPsec connection status logs
  - `trafficstatus/` - IPsec traffic validation logs
  - `<pod-name>_ipsec.conf` - IPsec configuration files per pod
  - `<pod-name>_ipsec.d/` - IPsec configuration directory per pod
  - `<pod-name>_libreswan.log` - Libreswan daemon logs per pod
  - **Priority**: Critical for IPsec tunnel failures and encryption issues

**Root Files**:
- `cluster_scale` - Network resource counts (services, endpoints, pods, network policies)
- `leader_nbdb` - Leader OVN Northbound database file (**legacy/single-zone OVN mode only**)
- `leader_sbdb` - Leader OVN Southbound database file (**legacy/single-zone OVN mode only**)
- `leader_ovnnb_status` - OVN Northbound raft cluster/status output (**legacy/single-zone OVN mode only**)
- `leader_ovnsb_status` - OVN Southbound raft cluster/status output (**legacy/single-zone OVN mode only**)
- `ovn_kubernetes_top_pods` - Resource usage of OVN-Kubernetes pods
- **Important**: `leader_nbdb`, `leader_sbdb`, `leader_ovnnb_status`, and `leader_ovnsb_status` are produced only when the cluster runs OVN in **legacy (single raft-clustered) mode**. In **interconnect mode** (multi-zone; each node is its own zone — the default in current OpenShift versions) there is no single NB/SB leader, so these four files **do not exist**; use `ovnk_database_store.tar.gz` (per-node DB copies) and `ovnk_extras_store.tar.gz` instead. Check `oc get node <sample-node> -o jsonpath='{.metadata.annotations.k8s\.ovn\.org/zone-name}'` — if it equals the node name, the cluster is in interconnect mode.
- **Priority**: Critical for OVN database corruption and leader election issues (legacy mode only)

**Collection Script**: `gather_network_logs_basics`

---

### 7. **`ingress_controllers/`** (Always Present)
**Purpose**: HAProxy configuration files from ingress controllers

**Subdirectories and Files**:
- `<ingress-controller-name>/<pod-name>/haproxy.config` - HAProxy configuration file per ingress pod
- **Priority**: Critical for ingress routing issues and load balancer configuration problems

**Collection Script**: `gather_haproxy_config`

---

### 8. **`nodes/`** (Always Present)
**Purpose**: Node-level performance and configuration data

**Subdirectories and Files**:
- **`<node-name>/`** - Per-node data containing:
  - `<node-name>_logs_kubelet.gz` - Kubelet journal logs per node (compressed)
  - `dmesg` - Kernel ring buffer (OOM kills, hardware faults, kernel panics)
  - `sysinfo.log` - System info snapshot log (df, ps, uptime, memory, disk usage)
  - `sysinfo.tgz` - Full system diagnostic archive (compressed)
  - `proc_cmdline` - Kernel boot parameters (`/proc/cmdline`)
  - `lscpu` - CPU topology / core-thread layout
  - `lspci` - PCI device inventory (NICs, accelerators, storage controllers)
  - `ethtool_channels` - NIC queue/channel configuration (`ethtool -l`)
  - `ethtool_features` - NIC offload/feature flags (`ethtool -k`)
  - `cpu_affinities.json` - Per-process CPU affinity/NUMA data
  - `irq_affinities.json` - IRQ-to-CPU affinity mapping
  - `podresources.json` - Kubelet pod resource allocation (device plugins, CPU manager)
  - `pods_info.json` - Pods scheduled on the node
  - **Priority**: Critical for node performance issues, NUMA/CPU-pinning, and hardware configuration problems
  - **Note**: This file list is exhaustive as of the current `gather_ppc` collection script; treat it as the authoritative reference for this directory rather than repeating it elsewhere. **To retrieve every file for a node in one shot, suggest the wildcard path `nodes/<node-name>/*`** — a bare `nodes/<node-name>/` (no trailing file or wildcard) does not resolve to any analyzable file and will be silently dropped.

**Root Files**:
- `debug` - Debug pod information and collection status
- `skipped_nodes.txt` - List of nodes where collection failed
- **Priority**: Medium for collection troubleshooting

**Collection Script**: `gather_ppc`

---

### 9. **`istio/`** (Conditional - if Istio/Service Mesh is enabled)
**Purpose**: Istio/Service Mesh and Gateway API data

**Subdirectories and Files**:
- `namespaces/<namespace>/<revision>/debug-syncz.json` - Istiod synchronization status per revision
- `namespaces/<namespace>/pods/<pod-name>/config_dump_istiod.json` - Istiod configuration dump per pod
- `namespaces/<namespace>/pods/<pod-name>/config_dump_proxy.json` - Envoy proxy configuration dump per pod
- `namespaces/<namespace>/pods/<pod-name>/proxy_stats` - Envoy proxy statistics per pod
- `cluster-scoped-resources/apiextensions.k8s.io/customresourcedefinitions/` - Gateway API CRDs
- **Priority**: Critical for service mesh connectivity and Gateway API issues

**Collection Script**: `gather_istio`

---

### 10. **`namespaces/`** (Always Present)
**Purpose**: Kubernetes resource data organized by namespace (created by `oc adm inspect`)

**Structure**: This directory follows the standard `oc adm inspect` output format:

**Per-Namespace Structure**:
- **`<namespace>/`** - Per-namespace resources
  - `<namespace>.yaml` - Namespace definition and metadata
  - **`core/`** - Core Kubernetes resources
    - `configmaps.yaml` - All ConfigMaps in namespace
    - `endpoints.yaml` - All Endpoints in namespace
    - `events.yaml` - All Events in namespace (Critical for event-driven diagnostics)
    - `persistentvolumeclaims.yaml` - All PVCs in namespace
    - `pods.yaml` - All Pod definitions in namespace
    - `replicationcontrollers.yaml` - All ReplicationControllers in namespace
    - `secrets.yaml` - All Secrets in namespace
    - `services.yaml` - All Services in namespace
    - `serviceaccounts.yaml` - All ServiceAccounts in namespace
  - **`apps/`** - Application workload resources
    - `daemonsets.yaml` - All DaemonSets in namespace
    - `deployments.yaml` - All Deployments in namespace
    - `replicasets.yaml` - All ReplicaSets in namespace
    - `statefulsets.yaml` - All StatefulSets in namespace
  - **`pods/<pod-name>/`** - Pod-specific data
    - `<pod-name>.yaml` - Pod definition and status
    - **`<container-name>/<container-name>/logs/`** - Container logs
      - `current.log` - Current container logs (Critical for runtime issues)
      - `previous.log` - Previous container logs (Critical for crash analysis)
      - `previous.insecure.log` - Previous container logs without security filtering
    - **Priority**: Critical for pod failures, container crashes, and application issues

**Key Namespaces Always Collected**:
- **`openshift-cluster-version/`** - Cluster version operator data (Critical for upgrade issues)
- **`openshift-etcd/`** - etcd pods and configuration (Critical for etcd issues)
- **`openshift-etcd-operator/`** - etcd operator data (Critical for etcd management issues)
- **`openshift-kube-apiserver/`** - Kubernetes API server pods (Critical for API issues)
  - **`pods/<pod-name>/kube-apiserver/kube-apiserver/api_priority_and_fairness/`**
    - `priority_levels` - API Priority and Fairness priority level configuration
    - `queues` - API request queue state
    - `requests` - Current API request state
    - **Priority**: Critical for API throttling and rate limiting issues
- **`openshift-apiserver/`** - OpenShift API server pods (Critical for OpenShift API issues)
- **`openshift-apiserver-operator/`** - OpenShift API server operator (Critical for API server management)
- **`openshift-authentication/`** - Authentication pods (Critical for auth issues)
- **`openshift-authentication-operator/`** - Authentication operator (Critical for auth management)
- **`openshift-kube-apiserver-operator/`** - Kubernetes API server operator (Critical for API server management)
- **`openshift-monitoring/`** - Monitoring stack pods (Critical for monitoring issues)
- **`openshift-ovn-kubernetes/`** - OVN-Kubernetes networking pods (Critical for OVN networking issues)
- **`openshift-network-operator/`** - Network operator (Critical for network configuration issues)
- **`openshift-machine-config-operator/`** - Machine Config Operator (Critical for node configuration issues)
- **`openshift-cluster-csi-drivers/`** - CSI driver pods (Critical for storage issues)
- **`default/`**, **`openshift/`**, **`kube-system/`** - Core namespaces

**Collection Script**: Main `gather` script and various specialized scripts

---

### 11. **`machine_config_ondisk/`** (Conditional - if degraded nodes exist)
**Purpose**: On-disk MachineConfig files from degraded nodes

**Subdirectories and Files**:
- **`<node-name>/`** - Per-node MachineConfig data
  - `mcs-machine-config-content.json` - Bootstrap configuration from Machine Config Server
  - `bootstrapconfigdiff` - Difference between bootstrap and current configuration
  - **Priority**: Critical for MachineConfig application failures and configuration drift

**Collection Script**: `gather_machineconfig_ondisk`

---

### 12. **`static-pods/`** (Always Present)
**Purpose**: Static pod logs (kube-apiserver startup and termination logs)

**Subdirectories and Files**:
- **`kube-apiserver/`** - Kube-apiserver static pod logs
  - `<node-name>-startup.log.gz` - API server startup logs per master node (compressed)
  - `<node-name>-termination.log.gz` - API server termination logs per master node (compressed)
  - **Priority**: Critical for API server crashes, startup failures, and graceful shutdown issues

**Collection Script**: `gather_kas_startup_termination_logs`

---

### 13. **`pod_network_connectivity_check/`** (Always Present)
**Purpose**: Pod network connectivity check resources

**Files**:
- `podnetworkconnectivitychecks.yaml` - All PodNetworkConnectivityCheck resources from openshift-network-diagnostics namespace
- **Priority**: Critical for pod-to-pod connectivity failures and network path validation

**Collection Script**: `gather_podnetworkconnectivitycheck`

---

### 14. **`cluster-scoped-resources/`** (Always Present)
**Purpose**: Cluster-level Kubernetes and OpenShift resources

**Subdirectories and Files**:
- **`config.openshift.io/`** - OpenShift configuration resources
  - `clusteroperators.yaml` - All ClusterOperator status (Critical for operator health)
  - `clusterversions.yaml` - Cluster version information (Critical for upgrade issues)
  - `infrastructures.yaml` - Infrastructure configuration (Critical for platform issues)
  - `networks.yaml` - Network configuration (Critical for network issues)
  - `authentications.yaml` - Authentication configuration (Critical for auth issues)
  - `nodes.yaml` - Node configuration (Critical for node issues)
  - `proxies.yaml` - Proxy configuration (Critical for connectivity issues)
  - `schedulers.yaml` - Scheduler configuration (Critical for scheduling issues)
  - `featuregates.yaml` - Feature gate configuration (Critical for feature issues)
  - `consoles.yaml` - Console configuration (Critical for console issues)
  - `oauths.yaml` - OAuth configuration (Critical for OAuth issues)

- **`core/`** - Core Kubernetes resources
  - `nodes/<node-name>.yaml` - Individual node definitions and status (Critical for node issues). **Path standard:** use `cluster-scoped-resources/core/nodes/*.yaml` or `nodes/<node-name>.yaml` — per-node files only; bare `core/nodes/` does not resolve.
  - `persistentvolumes/<pv-name>.yaml` - Individual PV definitions (Critical for storage issues)

- **`storage.k8s.io/`** - Storage resources
  - `storageclasses.yaml` - All StorageClass definitions (Critical for storage provisioning)
  - `volumeattachments/<attachment-name>.yaml` - Volume attachment status (Critical for mount issues)
  - `csidrivers.yaml` - CSI driver definitions (Critical for CSI issues)
  - `csinodes/<node-name>.yaml` - CSI node topology (Critical for storage node issues)

- **`rbac.authorization.k8s.io/`** - RBAC resources
  - `clusterroles.yaml` - All ClusterRole definitions (Critical for permission issues)
  - `clusterrolebindings.yaml` - All ClusterRoleBinding definitions (Critical for permission issues)

- **`apiextensions.k8s.io/customresourcedefinitions/`** - All CRD definitions
  - `<crd-name>.yaml` - Individual CRD definitions (Critical for custom resource issues)

- **`apiregistration.k8s.io/apiservices/`** - API service registrations
  - `<api-service-name>.yaml` - Individual API service definitions (Critical for API availability)

**Priority**: Critical for cluster-wide configuration and resource definition issues

---

## Resource Types Collected (via `oc adm inspect`)

The main `gather` script collects the following resource types:

### Cluster-Level Resources (Always Collected):
- `clusterversion` - Cluster version information
- `clusteroperators` - Cluster operator status
- `apiservices` - API service definitions
- `certificatesigningrequests` - Certificate signing requests
- `nodes` - Node information
- `storageclasses`, `persistentvolumes`, `volumeattachments` - Storage resources
- `networks.operator.openshift.io` - Network configuration
- `prioritylevelconfigurations`, `flowschemas` - API Priority and Fairness
- `clusterresourcequotas` - Cluster resource quotas

### Network Resources (Conditionally Collected):
- `nodenetworkstates`, `nodenetworkconfigurationpolicies` - NMState resources (if NMState enabled)
- `ippools`, `net-attach-def`, `multi-networkpolicy` - Multus resources (if Multus enabled)
- `egressips`, `clusteruserdefinednetworks` - OVN-Kubernetes resources (if OVN enabled)
- `hostsubnets` - OpenShift SDN resources (if SDN enabled)

### Storage Resources (Conditionally Collected):
- `csidrivers`, `csinodes` - CSI driver information
- `volumesnapshotclasses`, `volumesnapshotcontents` - Volume snapshots (if snapshot controller enabled)
- `csinodetopologies`, `cnsvspherevolumemigrations` - vSphere CSI resources (if vSphere platform)

---

## Collection Process

1. **Main Script** (`gather`):
   - Generates `version` file with must-gather tool version
   - Launches multiple collection scripts in parallel
   - Uses `oc adm inspect` for standard Kubernetes resource collection
   - Waits for all parallel processes to complete

2. **Parallel Collection**:
   - Most collection scripts run in background (`&`)
   - PIDs are tracked and waited upon
   - Each script creates its own directory structure
   - Failures in individual scripts don't stop overall collection

3. **Time Filtering**:
   - Supports `--since` and `--since-time` parameters
   - Applied to log collection via `MUST_GATHER_SINCE` and `MUST_GATHER_SINCE_TIME` environment variables
   - Affects audit logs and container logs

4. **Finalization**:
   - All scripts call `sync` to ensure data is written to disk
   - Data is then copied to the host system
   - Compressed files are created for large datasets

---

## File Formats and Analysis Priority

### Critical Files (Always Analyze First):
- **JSON Status Files**: `endpoint_health.json`, `endpoint_status.json`, `member_list.json`, `alarm_list.json` - Structured status data
- **Current Logs**: `current.log` files in pod containers - Active runtime issues
- **Events**: `events.yaml` files - Event-driven diagnostics
- **Cluster Operators**: `clusteroperators.yaml` - Overall cluster health

### Important Files (Analyze for Context):
- **Previous Logs**: `previous.log` files - Historical crash data
- **Configuration**: `.yaml` resource definitions - Configuration analysis
- **Service Logs**: `*_service.log` files - System service issues
- **Audit Logs**: `*-audit.log` files - API request tracing

### Supplementary Files (Analyze for Deep Dive):
- **Metrics**: `metrics.openmetrics` - Performance analysis
- **Status Dumps**: API priority and fairness dumps - Detailed state analysis
- **Database Files**: OVN database files - Network state analysis

---

## Mandatory File Combinations for Common Issues

### etcd Issues:
**Must Include**: `etcd_info/endpoint_health.json`, `etcd_info/member_list.json`, `etcd_info/alarm_list.json`, `namespaces/openshift-etcd/pods/*/logs/current.log`, `namespaces/openshift-etcd/core/events.yaml`

### API Server Issues:
**Must Include**: `audit_logs/kube-apiserver/<node-name>-audit.log`, `namespaces/openshift-kube-apiserver/pods/<pod-name>/<container-name>/<container-name>/logs/current.log`, `namespaces/openshift-kube-apiserver/pods/<pod-name>/<container-name>/<container-name>/logs/previous.log`, `static-pods/kube-apiserver/<node-name>-startup.log.gz`

### Pod Crash Issues:
**Must Include**: `namespaces/<namespace>/pods/<pod-name>/<container-name>/<container-name>/logs/current.log`, `namespaces/<namespace>/pods/<pod-name>/<container-name>/<container-name>/logs/previous.log`, `namespaces/<namespace>/core/events.yaml` (see Container-Aware Pod Paths section below for multi-container pods)

### Network Connectivity Issues:
**Must Include**: `pod_network_connectivity_check/podnetworkconnectivitychecks.yaml`, `network_logs/cluster_scale`, `namespaces/openshift-ovn-kubernetes/pods/*/logs/current.log` (if OVN)

### Storage Issues:
**Must Include**: `cluster-scoped-resources/storage.k8s.io/volumeattachments/`, `namespaces/<namespace>/core/persistentvolumeclaims.yaml`, `namespaces/openshift-cluster-csi-drivers/pods/*/logs/current.log`

---

## Container-Aware Pod Paths

Pod log directories include a `<container-name>/<container-name>/logs/` nesting. For pods with multiple containers, each container has its own log directory. Default to the **main application container** unless the user query specifies a different container.

### Single-Container Pod
```
namespaces/<namespace>/pods/<pod-name>/
├── <pod-name>.yaml
└── <container-name>/<container-name>/logs/
    ├── current.log
    ├── previous.log
    └── previous.insecure.log
```

### Multi-Container Pod (example: etcd)
```
namespaces/openshift-etcd/pods/etcd-<node-name>/
├── etcd-<node-name>.yaml
├── etcd/etcd/logs/                   # Main application container
│   ├── current.log
│   └── previous.log
├── etcd-metrics/etcd-metrics/logs/   # Metrics sidecar
│   ├── current.log
│   └── previous.log
├── etcd-readyz/etcd-readyz/logs/     # Readiness probe
│   ├── current.log
│   └── previous.log
├── etcdctl/etcdctl/logs/             # etcdctl utility
│   ├── current.log
│   └── previous.log
└── setup/setup/logs/                 # Init container
    ├── current.log
    └── previous.log
```

When investigating a pod issue, start with the **main application container** (typically the first or eponymous container). Only inspect sidecar or init container logs if the main container logs are inconclusive or the user asks about a specific container.

---

## File Size Awareness

Some files in the must-gather can be very large. Avoid parsing these unless the investigation specifically requires them:

| File / directory | Typical size | Notes |
|------------------|-------------|-------|
| `audit_logs/*-audit.log` | 100 MB – 1 GB+ per node | Only parse when investigating API auth, authorization, or request tracing |
| `monitoring/metrics/metrics.openmetrics` | 50 MB – 500 MB+ | Only parse for performance/resource analysis |
| `network_logs/ovnk_database_store.tar.gz` | 10 MB – 200 MB+ | Only decompress for OVN state analysis |
| `nodes/<node-name>/<node-name>_logs_kubelet.gz` | 10 MB – 100 MB+ | Only decompress for node-level kubelet investigation |
| `static-pods/kube-apiserver/*-termination.log.gz` | 5 MB – 50 MB+ | Only decompress for API server crash/shutdown analysis |

**Recommendation**: Start with smaller structured files (`events.yaml`, `endpoint_health.json`, `clusteroperators.yaml`) before moving to large logs. Use targeted keyword searches in large files rather than full parsing.

---

## Correlating with events.yaml

Each namespace contains a `core/events.yaml` file that records Kubernetes events. Use events as a timeline to correlate with log entries.

### Correlation strategies

- **By object**: Filter events by `involvedObject.name` and `involvedObject.kind` to find events related to a specific pod, node, deployment, or PVC.
- **By reason**: Filter by `reason` field to narrow to specific event types (e.g. `FailedScheduling`, `BackOff`, `Unhealthy`, `FailedMount`, `Pulling`, `Killing`).
- **By time**: Sort events by `lastTimestamp` or `firstTimestamp` to build a timeline of what happened before and after an issue.
- **By type**: Filter by `type` field — `Warning` events indicate problems; `Normal` events confirm expected operations.

### Example correlation workflow

1. **Start** with `namespaces/<namespace>/core/events.yaml` — scan for `Warning` type events.
2. **Identify** the affected object (pod, node, PVC) from `involvedObject`.
3. **Find** the corresponding pod logs at `namespaces/<namespace>/pods/<pod-name>/<container-name>/<container-name>/logs/current.log`.
4. **Match timestamps** between events and log entries to pinpoint the root cause.
5. **Cross-reference** with `cluster-scoped-resources/config.openshift.io/clusteroperators.yaml` if the events suggest operator-level issues.

### Key event fields

| Field | Use |
|-------|-----|
| `involvedObject.name` | Which resource the event is about |
| `involvedObject.kind` | Resource type (Pod, Node, PVC, etc.) |
| `reason` | Short machine-readable reason (e.g. `FailedScheduling`) |
| `message` | Human-readable description |
| `type` | `Normal` or `Warning` |
| `firstTimestamp` / `lastTimestamp` | When the event first/last occurred |
| `count` | How many times the event repeated |

---

## Notes

- **Conditional Collections**: Some directories only exist if specific features are enabled (Windows nodes, Istio, SR-IOV, etc.)
- **Compressed Files**: Some files are collected in compressed form (`.gz`, `.tar.gz`). Always reference them by their actual on-disk name including the compression extension (e.g. `<node-name>-termination.log.gz`, `<node-name>_logs_kubelet.gz`, `ovnk_database_store.tar.gz`)
- **Time Sensitivity**: Log files are time-sensitive; check collection time window via `timestamp` file
- **Cross-Component Dependencies**: etcd issues often require API server analysis; networking issues may need container runtime logs
- **Platform Variations**: Some collections are platform-specific (vSphere, ARO, bare metal)
- **Operator-Specific Data**: Additional namespaces may exist for optional operators (SR-IOV, MetalLB, NMState, etc.)

---