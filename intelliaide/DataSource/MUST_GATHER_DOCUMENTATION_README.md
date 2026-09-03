---
# Must-Gather Documentation Suite

This documentation suite provides comprehensive information about the OpenShift must-gather tool's output structure and how to use it for problem diagnosis. This guide ensures consistent LLM routing and reduces variance in file path recommendations across different models.

## Documentation Files

### 1. **MUST_GATHER_STRUCTURE.md**
**Purpose**: Detailed description of the directory structure and file purposes

**Contents**:
- Complete directory tree with descriptions
- File formats and contents
- Collection process overview
- Resource types collected

**Use When**: You need to understand what data is collected and where it's stored

---

### 2. **MUST_GATHER_ROUTING_GUIDE.md**
**Purpose**: Problem-based routing guide for LLM-assisted diagnosis

**Contents**:
- 29 problem categories with detailed mappings
- Keywords for each problem type
- Primary directories and files for each category
- Related resources cross-references
- Routing decision tree
- Quick reference table

**Use When**: You have a problem statement and need to identify relevant files

**Problem Categories Covered** (29 categories):
1. API Server & Authentication Issues
2. Cluster Operator & Control Plane Issues
3. Networking & Connectivity Issues
4. Storage & Volume Issues
5. Node & Machine Configuration Issues
6. Pod & Container Issues
7. Performance & Resource Issues
8. Security & Audit Issues
9. Service Mesh & Istio Issues (conditional)
10. Monitoring & Metrics Issues
11. Windows Node Issues (conditional)
12. Platform-Specific Issues (vSphere, ARO, bare-metal)
13. etcd Issues
14. Storage Version Migration Issues
15. IPsec & Network Security Issues
16. External DNS / API Resolution (infrastructure)
17. Enterprise Proxy / Image Pull / TLS Trust
18. Machine API / Node Provisioning
19. Image Registry Issues
20. Ingress / Routes
21. Cluster Upgrade / CVO
22. Workloads (Deployments / Jobs)
23. Scheduler / Controller Manager
24. Admission Webhooks
25. RHOSO / OpenStack on OpenShift
26. Insights / Compliance
27. KubeletConfig / SystemMemoryExceedsReservation
28. OLM / OperatorHub / Subscriptions
29. Console / FeatureGate

---

### 3. **MUST_GATHER_INDEX.md**
**Purpose**: Quick reference index for fast keyword-based lookups

**Contents**:
- Directory structure quick index
- Keyword to directory mapping
- File type patterns
- Common problem patterns
- Search strategy for LLMs

**Use When**: You need quick lookups or keyword matching

---

## Standardization Rules for LLM Outputs

### Path Format Standards

1. **Use actual on-disk file extensions**: `.log`, `.yaml`, `.json` for uncompressed files; `.log.gz`, `.gz`, or `.tar.gz` for compressed files (e.g. `*-termination.log.gz`, `*_logs_kubelet.gz`, `ovnk_database_store.tar.gz`)
2. **Wildcard substitution rules**:
   - `<namespace>` for actual namespace names
   - `<pod-name>` for actual pod names
   - `<node-name>` for actual node names
   - `*` only when multiple files of same type exist
3. **Consistent path separators**: Always use forward slashes `/`
4. **Base path convention**: All paths relative to `<must-gather-root>/<content-folder>/`

### Mandatory File Inclusion Rules

1. **For pod issues**: MUST include both `current.log` AND `previous.log` from container logs
2. **For pod/operator logs**: Always list **both** `pods/<pod-name>/<container-name>/<container-name>/logs/current.log` and `pods/<pod-name>/<container-name>/<container-name>/logs/previous.log` as **two separate lines** in the output (never combine them). This applies to the anchor namespace and to cross-component namespaces (e.g. storage migration: include migrator previous.log and cluster-version previous.log).
3. **For operator issues**: MUST include both pod logs AND events from the operator namespace
4. **For etcd issues**: MUST include ALL files from `etcd_info/` directory
5. **For networking issues**: MUST include connectivity checks AND DNS/API resolution files (`infrastructures.yaml`, `dnses.yaml`) before treating OVN/CRI-O as primary
6. **For NotReady masters / API unreachable**: MUST include Section 16 external DNS/API set at HIGH priority before OVN/CRI-O
7. **For ImagePull / x509 / proxy**: MUST include `proxies.yaml` and `images.yaml`
8. **For API server issues**: MUST include both audit logs AND pod logs AND priority/fairness data; also infrastructures/dnses when unreachable
9. **For SystemMemoryExceedsReservation / autoSizingReserved**: MUST include kubeletconfigs and validate field placement before monitoring primacy
10. **List length**: Prefer the most diagnostic paths; do not enumerate every possible path.

### Minimum diagnostic set by component (always include when relevant)

| Component | Minimum set (paths) |
|-----------|---------------------|
| **External DNS / API VIP** | `infrastructures.yaml`; `dnses.yaml`; `podnetworkconnectivitychecks.yaml`; `core/nodes/*.yaml`; kubelet + NetworkManager service logs; `namespaces/openshift-dns/pods/*/*/*/logs/current.log` |
| **NotReady master** | Node files (`core/nodes/*.yaml`) **plus** External DNS / API VIP set **before** OVN/CRI-O |
| **Enterprise proxy / TLS** | `proxies.yaml`; `images.yaml`; kubelet + crio service logs; image-registry events when pull-related |
| **Authentication / login** | `authentications/`; `oauths.yaml`; oauth pods current+previous; oauth audit; `proxies.yaml` if external IdP |
| **ImagePullBackOff** | `images.yaml`; `proxies.yaml`; `namespaces/openshift-image-registry/`; namespace events; crio logs |
| **Machine not joining** | `namespaces/openshift-machine-api/` events+logs; `core/nodes/*.yaml`; `infrastructures.yaml` |
| **etcd** | `etcd_info/endpoint_health.json`, `endpoint_status.json`, `member_list.json`, `alarm_list.json`, `object_count.json`; `namespaces/openshift-etcd/core/events.yaml`; `namespaces/openshift-etcd/pods/*/logs/current.log` and `previous.log`; `namespaces/openshift-etcd-operator/pods/*/logs/current.log` and `previous.log`; `audit_logs/etcd/*-audit.log`; for API impact: `namespaces/openshift-kube-apiserver/pods/*/logs/current.log` and `previous.log`; infrastructures/dnses when dial failures |
| **API server** | `infrastructures.yaml`, `dnses.yaml`, connectivity checks (when unreachable); `namespaces/openshift-kube-apiserver/core/events.yaml`; pods logs current+previous; APF queues; `audit_logs/kube-apiserver/*-audit.log`; static-pod startup/termination; cross: `etcd_info/endpoint_health.json` |
| **Storage migration** | `namespaces/openshift-kube-storage-version-migrator/core/events.yaml`; pods logs current+previous; `storageversionmigrations.yaml`; `storageclasses.yaml`; cross: CVO + kube-apiserver logs |
| **OVN-Kubernetes / alerts** | After DNS/API checked: OVN events + pod logs; `leader_ovnnb_status`, `leader_ovnsb_status` (legacy OVN mode only — use `ovnk_database_store.tar.gz`/`ovnk_extras_store.tar.gz` in interconnect mode), `ovn_kubernetes_top_pods`; monitoring alertmanager/prometheus; connectivity checks |
| **IPsec + OVN traffic** | `network_logs/ipsec/trafficstatus/`, `status/`; OVN pod logs/events; network-operator logs/events |
| **RHOSO / OpenStack** | Section 16 first if NotReady; `namespaces/openstack/` events + pod logs; clusteroperators; infrastructures/dnses/proxies/images |
| **Ingress / Routes** | haproxy.config; openshift-ingress + ingress-operator logs/events; infrastructures + dnses |
| **Upgrade / CVO** | clusterversions + clusteroperators + CVO events/logs; MCP if drain blocked |
| **Scheduler / Pending** | openshift-kube-scheduler logs/events; nodes/; FailedScheduling events |
| **Admission webhooks** | ALL mutating/validating webhookconfiguration CRs; per-webhook `timeoutSeconds`/`failurePolicy`/endpoints; webhook ns logs; literal-match timeout in user error; apiserver audit only supporting |
| **Insights** | insights-data/; openshift-insights logs/events |
| **Windows nodes** | host_service_logs/windows/log_files/* |
| **Service Mesh** | istio/ config dumps + networking.istio.io/ |
| **KubeletConfig / SystemMemoryExceedsReservation** | `machineconfiguration.openshift.io/kubeletconfigs/`; validate `spec.autoSizingReserved` (NOT under `spec.kubeletConfig`); machineconfigs/MCPs; kubelet logs; nodes capacity/allocatable — monitoring only after CR placement OK |
| **OLM / OperatorHub** | `namespaces/openshift-operator-lifecycle-manager/` logs/events; `namespaces/openshift-marketplace/` logs/events; subscriptions/installplans/CSVs in operator namespace; CRDs |
| **Console / FeatureGate** | `config.openshift.io/consoles.yaml`; `config.openshift.io/featuregates.yaml`; `namespaces/openshift-console/` + `openshift-console-operator/` logs/events; authentications.yaml; infrastructures + dnses (route DNS) |

### DNS artifact disambiguation (do not confuse these four files)

| File | What it shows | Use for external-DNS RCA? |
|---|---|---|
| `config.openshift.io/dnses.yaml` | Cluster baseDomain / external DNS config | **Yes — required** |
| `config.openshift.io/clusteroperators.yaml` (dns slice) | DNS *operator* health only | No — operator status ≠ resolution failure |
| `operator.openshift.io/dnses/default.yaml` | CoreDNS internal upstream resolvers | No — internal DNS only |
| CRD `dnses.operator.openshift.io.yaml` | Schema only | No — never evidence |

### Problem phrase → primary anchor and paths (for accurate file selection)

| **Two masters NotReady, API unreachable, missing DNS, Nova/RHOSO down** | External DNS / API (16) + RHOSO (25) | `infrastructures.yaml`; `dnses.yaml`; connectivity checks; kubelet_service.log; CoreDNS; `namespaces/openstack/`; then etcd/API/OVN only as cascade |
| **x509 unknown authority / ImagePull through corporate proxy** | Proxy / TLS (17) | `proxies.yaml`; `images.yaml`; kubelet + crio logs; image-registry events |
| **Login / OAuth / IdP failure** | Authentication (1) | `authentications/`; oauth pods; oauth audit; `proxies.yaml` if external IdP |
| **Machine not joining / MachineSet stuck** | Machine API (18) | `openshift-machine-api` events+logs; nodes; infrastructures |
| **Route / *.apps URL failure** | Ingress (20) | haproxy.config; ingress + ingress-operator; dnses/infrastructures — not OVN-only |
| **Upgrade stuck / CVO Progressing** | Upgrade (21) | clusterversions; clusteroperators; CVO logs; MCP if needed |
| **Pods Pending / FailedScheduling** | Scheduler (23) | kube-scheduler logs; nodes; namespace events |
| **Webhook denying creates / MutatingAdmissionWebhook timeout** | Admission (24) | Inventory ALL MWCs/VWCs; match error `Ns` to `timeoutSeconds: N`; check endpoints; prefer remove/disable failing webhooks — not apiserver CrashLoop as primary |
| **etcdGRPCRequestsSlow has spiked** (e.g. Azure CI) | etcd (13) | `etcd_info/*.json`; `namespaces/openshift-etcd/` and `openshift-etcd-operator/` (events, pods/*/logs/current and previous); `audit_logs/etcd/*-audit.log`; `monitoring/metrics/metrics.openmetrics`; `nodes/*/*`; API server pod logs |
| **kube-storage-version-migrator Available=False, KubeStorageVersionMigrator_Deploying during updates** | Storage migration (14) | `namespaces/openshift-kube-storage-version-migrator/` (core/events.yaml, pods/*/logs/current and previous, apps/deployments.yaml, batch/jobs.yaml); `cluster-scoped-resources/migration.k8s.io/storageversionmigrations.yaml`; `namespaces/openshift-cluster-version/` (events, pod logs); `etcd_info/`, kube-apiserver logs |
| **OVNKubernetesResourceRetryFailure, component readiness, bz-networking invariant, alert at or above info** | Networking / OVN (3) after DNS check | DNS/API set first; then `namespaces/openshift-ovn-kubernetes/` (events, pods/*/logs/current and previous); `network_logs/leader_ovnnb_status`, `leader_ovnsb_status` (legacy OVN mode only), `ovn_kubernetes_top_pods`; `monitoring/alertmanager/`, `monitoring/prometheus/`; connectivity checks |
| **sig-network Feature:IPsec, check traffic with IPsec, ovn-kubernetes + IPsec** | IPsec (15) + OVN | `network_logs/ipsec/trafficstatus/`, `network_logs/ipsec/status/`, `network_logs/ipsec/*.conf`; `namespaces/openshift-ovn-kubernetes/` (events, pods/*/logs/current and previous); `namespaces/openshift-network-operator/` (pod logs, events) |
| **Loss of APIServer networking, etcd quorum, high CPU, mass test failure** | Multi-component (16 + 1 + 13 + 3) | External DNS/API first; then API server + etcd + networking + metrics/nodes/kubelet + clusteroperators |
| **Windows node unhealthy** | Windows (11/27) | `host_service_logs/windows/log_files/*` |
| **Istio / Service Mesh** | Service Mesh (9/28) | istio/ config dumps — not OVN-only |
| **Insights archive / compliance** | Insights (26) | insights-data/; openshift-insights |
| **SystemMemoryExceedsReservation / autoSizingReserved misplaced** | KubeletConfig (27/29) | `kubeletconfigs/` FIRST — validate `spec.autoSizingReserved` placement; do not lead with Prometheus/cAdvisor; MachineConfig `*auto-sizing*` filenames alone are not root cause |

### Cross-Component Dependencies

When analyzing these components, ALWAYS include related components:

- **etcd issues** → Include API server logs and cluster operator status; include infrastructures/dnses when peer dial failures
- **Networking issues** → Include DNS (internal + external config) and connectivity checks first; CRI-O/OVN when CNI/runtime implicated
- **NotReady masters / API unreachable** → External DNS/API set before OVN/etcd deep-dives
- **ImagePull / x509** → proxies.yaml + images.yaml before runtime-only blame
- **SystemMemoryExceedsReservation** → KubeletConfig / `autoSizingReserved` placement before monitoring primacy
- **MutatingAdmissionWebhook / webhook timeout** → full webhook CR inventory + timeoutSeconds literal match + endpoints before apiserver/OVN cascade primacy
- **Storage issues** → Include both CSI driver logs and pod mount logs
- **Performance issues** → Include both metrics data and node-level diagnostics
- **Operator issues** → Include both operator namespace and cluster operator status
- **Machine not joining** → Machine API namespace + infrastructures + node/kubelet

---

## Critical Files Matrix

### Always Present Files
These files exist in every must-gather collection:

| Directory | Critical Files | Purpose |
|-----------|---------------|---------|
| `etcd_info/` | `endpoint_health.json`, `endpoint_status.json`, `member_list.json`, `alarm_list.json`, `object_count.json` | etcd cluster health |
| `cluster-scoped-resources/config.openshift.io/` | `clusteroperators.yaml`, `infrastructures.yaml`, `networks.yaml`, `dnses.yaml`, `proxies.yaml`, `images.yaml` | Cluster + infra prerequisites |
| `namespaces/openshift-kube-apiserver/` | `core/events.yaml`, `core/pods.yaml` | API server status |
| `host_service_logs/masters/` | `kubelet_service.log`, `crio_service.log` | Master node services |
| `host_service_logs/workers/` | `kubelet_service.log`, `crio_service.log` | Worker node services |

### Conditionally Present Files
These files only exist when specific features are enabled:

| Directory | Files | Condition |
|-----------|-------|-----------|
| `audit_logs/etcd/` | `*-audit.log` | Audit logging enabled |
| `network_logs/ipsec/` | `*_ipsec.conf`, `status/*` | IPsec enabled |
| `namespaces/openshift-sriov-network-operator/` | All files | SR-IOV operator installed |
| `host_service_logs/windows/` | All files | Windows nodes present |
| `istio/` | All files | Service mesh enabled |

### Service Log Inventory

**Master Node Service Logs** (in `host_service_logs/masters/`):
- `kubelet_service.log` - Kubelet service logs
- `crio_service.log` - Container runtime logs
- `NetworkManager_service.log` - Network manager logs
- `machine-config-daemon-firstboot_service.log` - MCO first boot logs
- `machine-config-daemon-host_service.log` - MCO host service logs
- `openvswitch_service.log` - Open vSwitch logs
- `ovs-configuration_service.log` - OVS configuration logs
- `ovs-vswitchd_service.log` - OVS daemon logs
- `ovsdb-server_service.log` - OVS database server logs
- `rpm-ostreed_service.log` - RPM OSTree daemon logs
- `ostree-finalize-staged_service.log` - OSTree staged-deployment finalization logs

**Worker Node Service Logs** (in `host_service_logs/workers/`):
- Same as master nodes except machine-config-daemon may have different behavior

**Windows Node Service Logs** (in `host_service_logs/windows/log_files/`):
- `kubelet/kubelet.log` - Windows kubelet logs
- `kube-proxy/kube-proxy.log` - Windows kube-proxy logs
- `containerd/containerd.log` - Windows container runtime logs
- `hybrid-overlay/hybrid-overlay.log` - Hybrid overlay networking logs
- `wicd/` - Windows Instance Config Daemon logs
- `csi-proxy/csi-proxy.log` - CSI proxy logs

---

## LLM Routing Workflow

### Step 1: Problem Classification
1. Extract keywords from user problem statement
2. Map keywords to primary problem category using `MUST_GATHER_INDEX.md`
3. Identify secondary categories for cross-component issues

### Step 2: Mandatory File Selection
1. Select critical files from the primary category using `MUST_GATHER_ROUTING_GUIDE.md`
2. Apply mandatory inclusion rules (current.log + previous.log, etc.)
3. Add cross-component dependencies based on problem type

### Step 3: Path Standardization
1. Apply path format standards (decompressed extensions only)
2. Use consistent wildcard substitution
3. Ensure all paths are relative to `<must-gather-root>/<content-folder>/`

### Step 4: Conflict Resolution
When multiple problem categories overlap:
1. **Primary category**: The most specific match takes precedence
2. **Secondary categories**: Include related files but mark as secondary
3. **Cross-dependencies**: Always include mandatory cross-component files

### Example Workflow Application

**User Query**: "etcd cluster is unhealthy and API server is slow"

**Step 1**: Keywords ["etcd", "unhealthy", "api server", "slow"] → Primary: etcd Issues, Secondary: API Server Issues

**Step 2**: Mandatory files:
- Primary (etcd): ALL files from `etcd_info/`
- Secondary (API): `audit_logs/kube-apiserver/`, `namespaces/openshift-kube-apiserver/pods/*/logs/`
- Cross-dependency: API priority and fairness data

**Step 3**: Standardized paths:
- `etcd_info/endpoint_health.json`
- `namespaces/openshift-kube-apiserver/pods/<pod-name>/<container-name>/<container-name>/logs/current.log`
- `static-pods/kube-apiserver/<node-name>-startup.log.gz` (compressed — use actual on-disk name)

**Step 4**: Final output includes both etcd and API server files with clear categorization

---

## Cross-Directory Dependencies

### etcd Issues
**Primary**: `etcd_info/`, `namespaces/openshift-etcd/`
**Required Dependencies**: 
- `namespaces/openshift-kube-apiserver/` (API server impact)
- `cluster-scoped-resources/config.openshift.io/clusteroperators.yaml` (operator status)
- `audit_logs/etcd/` (if audit enabled)

### Networking Issues
**Primary**: `infrastructures.yaml`, `dnses.yaml`, `pod_network_connectivity_check/`, then `network_logs/`
**Required Dependencies**:
- `namespaces/openshift-dns/` (rule out internal DNS)
- `namespaces/openshift-ovn-kubernetes/` or `namespaces/openshift-sdn/` when CNI implicated
- `host_service_logs/*/NetworkManager_service.log`
- `host_service_logs/*/kubelet_service.log` for API/lease failures
- `host_service_logs/*/crio_service.log` when runtime/CNI implicated (not default-primary for every network case)
- `proxies.yaml` / `images.yaml` when x509/ImagePull present

### Storage Issues
**Primary**: `cluster-scoped-resources/storage.k8s.io/`, `namespaces/openshift-cluster-csi-drivers/`
**Required Dependencies**:
- `namespaces/<namespace>/pods/<pod>/logs/` (for mount failures)
- `namespaces/<namespace>/core/events.yaml` (for storage events)
- `cluster-scoped-resources/storage.k8s.io/volumeattachments/`

### Performance Issues
**Primary**: `monitoring/metrics/`, `nodes/`
**Required Dependencies**:
- `namespaces/openshift-kube-apiserver/pods/*/api_priority_and_fairness/`
- `host_service_logs/*/kubelet_service.log`
- `monitoring/prometheus/status/tsdb.json`

### Operator Issues
**Primary**: `namespaces/<operator-namespace>/`
**Required Dependencies**:
- `cluster-scoped-resources/config.openshift.io/clusteroperators.yaml`
- `namespaces/<operator-namespace>/core/events.yaml`
- `namespaces/<operator-namespace>/pods/*/logs/current.log`
- `namespaces/<operator-namespace>/pods/*/logs/previous.log`

---

## Key Concepts

### Directory Organization
- **Base Path**: All data under `<must-gather-root>/<content-folder>/` (user supplies root; one child folder, any name, holds the content)
- **Namespace-based**: Most resources organized by namespace
- **Cluster-scoped**: Cluster-level resources in `cluster-scoped-resources/`
- **Feature-specific**: Some directories only exist if features enabled

### File Types
- **Logs**: `.log` for most logs; some are compressed as `.log.gz` (e.g. static-pod startup/termination) or `.gz` (e.g. kubelet logs). Always use the actual on-disk extension.
- **Status**: `.json` - Health, status, configuration state
- **Config**: `.yaml`, `.config` - Resource definitions, configurations
- **Metrics**: `.openmetrics` - Performance and resource metrics
- **Archives**: `.tar.gz` - Compressed archives (e.g. `ovnk_database_store.tar.gz`)

### Collection Process
- **Parallel Execution**: Multiple collection scripts run simultaneously
- **Time Filtering**: Supports `--since` and `--since-time` parameters
- **Conditional Collection**: Some data only collected if features enabled
- **Error Handling**: Continues collection even if some parts fail

---

## Problem Diagnosis Workflow

### 1. Identify Problem Category
Match user keywords to problem categories in routing guide using standardized keyword mapping.

### 2. Select Primary Directories
Use routing guide to identify most relevant directories, applying mandatory inclusion rules.

### 3. Prioritize Files
Within directories, prioritize using this hierarchy:
1. **Critical files** (from matrix above)
2. **Logs** for runtime issues (`current.log`, `previous.log`)
3. **Status** for state problems (`.json` files)
4. **Config** for configuration issues (`.yaml` files)
5. **Events** for event-driven problems (`events.yaml`)

### 4. Apply Cross-References
Include mandatory cross-component dependencies based on problem type.

### 5. Standardize Output
Apply path format standards and ensure consistent wildcard usage.

---

## Quick Reference Tables

### Most Common Problems → Standardized File Paths

| Problem | Primary Files | Secondary Files |
|---------|--------------|----------------|
| SystemMemoryExceedsReservation | `kubeletconfigs/` + validate `autoSizingReserved` at `spec.autoSizingReserved` | machineconfigs, kubelet logs, nodes; monitoring only if CR OK |
| Masters NotReady / API unreachable | `infrastructures.yaml`, `dnses.yaml`, connectivity checks, `kubelet_service.log` | etcd_info/, API server logs, OVN (cascade) |
| External DNS / no such host | `infrastructures.yaml`, `dnses.yaml`, kubelet logs, CoreDNS events | NetworkManager (symptom) |
| x509 / ImagePull / proxy | `proxies.yaml`, `images.yaml`, kubelet+crio logs | image-registry events |
| Pod crash | `namespaces/<namespace>/pods/<pod-name>/<container-name>/<container-name>/logs/current.log`, `previous.log` | `namespaces/<namespace>/core/events.yaml` |
| Network issue (CNI) | connectivity checks, `dnses.yaml`, `infrastructures.yaml` | OVN pod logs, `network_logs/` |
| API failure | infrastructures/dnses + connectivity, apiserver logs, audit | APF queues, etcd health |
| Operator degraded | `clusteroperators.yaml` | operator namespace pod logs |
| Node not ready | node YAML, kubelet logs; if masters: DNS/API set | `nodes/<node-name>/*`, Machine API |
| Machine not joining | `openshift-machine-api` events+logs | infrastructures, nodes |
| Storage mount | pod logs, namespace events | volumeattachments, CSI logs |
| Performance | `metrics.openmetrics`, `nodes/<node-name>/*` | APF queues |
| etcd issue | `etcd_info/*.json`, etcd pod logs | API server logs, infrastructures,dnses |
| Auth / login | authentications/, oauth pods | proxies.yaml, oauth audit |
| Registry / ImagePullBackOff | images.yaml, proxies.yaml, image-registry | crio logs, namespace events |

### Wildcard Substitution Rules

| Wildcard | Substitution Rule | Example |
|----------|------------------|---------|
| `<namespace>` | Replace with actual namespace name | `openshift-etcd`, `default`, `kube-system` |
| `<pod-name>` | Replace with actual pod name | `etcd-master-0`, `apiserver-9f5b9f9d4-5djkq` |
| `<node-name>` | Replace with actual node name | `ip-10-0-122-129.us-east-2.compute.internal` |
| `*` | Use when multiple files of same type exist | `pods/*/<container>/<container>/logs/current.log` |
| `<operator-namespace>` | Replace with operator's namespace | `openshift-machine-config-operator` |

---

## Version Information

- **Must-Gather Version**: Check `<must-gather-root>/<content-folder>/version` in output
- **Collection Scripts**: Located in `collection-scripts/` directory
- **Documentation Version**: Based on must-gather-main repository

---

## Additional Resources

- **Original Enhancement**: See `must-gather.md` for design details
- **Collection Scripts**: See `collection-scripts/` for implementation
- **OpenShift Documentation**: [Official must-gather docs](https://docs.openshift.com/)

---

